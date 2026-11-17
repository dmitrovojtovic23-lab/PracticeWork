import random
import re

import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset

random.seed(42)
torch.manual_seed(42)

DATA = [
    ("How can I reset my password?", "You can reset your password in settings."),
    ("How do I change my email?", "You can update it in your profile settings."),
    ("My order is delayed", "Your order may take a bit longer, sorry for the delay."),
    ("I need help with my account", "We can help you with that."),
    ("Can I cancel my subscription?", "Yes, you can cancel anytime from your account."),
    ("What is the refund policy?", "You can request a refund within 30 days."),
    ("I want to update my shipping address", "You can change it in your account settings."),
    ("Where do I find my invoice?", "Your invoice is available in the billing section."),
    ("How can I contact support?", "You can contact support from the help center."),
    ("My account is locked", "Please reset your password or contact support."),
]

BATCH_SIZE = 4
EPOCHS = 100
EMBED_DIM = 32
HIDDEN_SIZE = 64
LEARNING_RATE = 1e-3


def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    return text.split()


def build_vocab(pairs):
    tokens = []
    for src, tgt in pairs:
        tokens.extend(tokenize(src))
        tokens.extend(tokenize(tgt))
    vocab = {"<pad>": 0, "<sos>": 1, "<eos>": 2}
    for token in sorted(set(tokens)):
        if token not in vocab:
            vocab[token] = len(vocab)
    idx_to_token = {idx: token for token, idx in vocab.items()}
    return vocab, idx_to_token


def encode_sequence(text, vocab):
    tokens = tokenize(text)
    seq = [vocab["<sos>"]]
    seq.extend(vocab[token] for token in tokens)
    seq.append(vocab["<eos>"])
    return seq


vocab, idx_to_token = build_vocab(DATA)
MAX_LEN = max(len(encode_sequence(src, vocab)) for src, _ in DATA)
MAX_LEN = max(MAX_LEN, max(len(encode_sequence(tgt, vocab)) for _, tgt in DATA))


class ChatDataset(Dataset):
    def __init__(self, pairs):
        self.pairs = []
        for src, tgt in pairs:
            src_seq = encode_sequence(src, vocab)
            tgt_seq = encode_sequence(tgt, vocab)
            if len(src_seq) > MAX_LEN:
                src_seq = src_seq[:MAX_LEN]
            if len(tgt_seq) > MAX_LEN:
                tgt_seq = tgt_seq[:MAX_LEN]
            self.pairs.append((torch.tensor(src_seq, dtype=torch.long), torch.tensor(tgt_seq, dtype=torch.long)))

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        return self.pairs[idx]


def collate_fn(batch):
    src_batch = [item[0] for item in batch]
    tgt_batch = [item[1] for item in batch]
    src = pad_sequence(src_batch, batch_first=True, padding_value=vocab["<pad>"])
    tgt = pad_sequence(tgt_batch, batch_first=True, padding_value=vocab["<pad>"])
    return src, tgt


train_loader = DataLoader(ChatDataset(DATA), batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)


class LSTMSeq2Seq(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=vocab["<pad>"])
        self.encoder = nn.LSTM(embed_dim, hidden_size, num_layers=2, batch_first=True, dropout=0.1)
        self.decoder = nn.LSTM(embed_dim, hidden_size, num_layers=2, batch_first=True, dropout=0.1)
        self.output = nn.Linear(hidden_size, vocab_size)

    def forward(self, src, tgt):
        src_emb = self.embedding(src)
        _, hidden = self.encoder(src_emb)
        tgt_input = tgt[:, :-1]
        dec_emb = self.embedding(tgt_input)
        dec_out, _ = self.decoder(dec_emb, hidden)
        return self.output(dec_out)

    def predict(self, src, max_len=12):
        self.eval()
        if src.dim() == 1:
            src = src.unsqueeze(0)
        with torch.no_grad():
            src_emb = self.embedding(src)
            _, hidden = self.encoder(src_emb)
            current = torch.tensor([[vocab["<sos>"]]], device=src.device, dtype=torch.long)
            result = [vocab["<sos>"]]
            for _ in range(max_len):
                dec_emb = self.embedding(current)
                dec_out, hidden = self.decoder(dec_emb, hidden)
                logits = self.output(dec_out[:, -1, :])
                idx = int(logits.argmax(dim=-1))
                result.append(idx)
                if idx == vocab["<eos>"]:
                    break
                current = torch.tensor([[idx]], device=src.device, dtype=torch.long)
            return result


class TransformerSeq2Seq(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, max_len):
        super().__init__()
        self.src_embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=vocab["<pad>"])
        self.tgt_embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=vocab["<pad>"])
        self.pos_embedding = nn.Embedding(max_len + 4, embed_dim)
        self.transformer = nn.Transformer(
            d_model=embed_dim,
            nhead=4,
            num_encoder_layers=2,
            num_decoder_layers=2,
            dim_feedforward=hidden_size,
            dropout=0.1,
            batch_first=True,
        )
        self.output = nn.Linear(embed_dim, vocab_size)

    def position(self, seq_len, batch_size, device):
        positions = torch.arange(seq_len, device=device).unsqueeze(0).repeat(batch_size, 1)
        return self.pos_embedding(positions)

    def forward(self, src, tgt):
        src_emb = self.src_embedding(src) + self.position(src.size(1), src.size(0), src.device)
        tgt_in = tgt[:, :-1]
        tgt_emb = self.tgt_embedding(tgt_in) + self.position(tgt_in.size(1), tgt_in.size(0), tgt.device)
        dec_out = self.transformer(src_emb, tgt_emb)
        return self.output(dec_out)

    def predict(self, src, max_len=12):
        self.eval()
        if src.dim() == 1:
            src = src.unsqueeze(0)
        with torch.no_grad():
            src_emb = self.src_embedding(src) + self.position(src.size(1), src.size(0), src.device)
            memory = self.transformer.encoder(src_emb)
            current = torch.tensor([[vocab["<sos>"]]], device=src.device, dtype=torch.long)
            result = [vocab["<sos>"]]
            for _ in range(max_len):
                tgt_emb = self.tgt_embedding(current) + self.position(current.size(1), current.size(0), src.device)
                dec_out = self.transformer.decoder(tgt_emb, memory)
                logits = self.output(dec_out[:, -1, :])
                idx = int(logits.argmax(dim=-1))
                result.append(idx)
                if idx == vocab["<eos>"]:
                    break
                current = torch.cat((current, torch.tensor([[idx]], device=src.device)), dim=1)
            return result


def decode_tokens(token_ids):
    words = []
    for token_id in token_ids:
        token = idx_to_token.get(token_id, "<pad>")
        if token in {"<pad>", "<sos>"}:
            continue
        if token == "<eos>":
            break
        words.append(token)
    return " ".join(words)


def train_model(model, epochs):
    criterion = nn.CrossEntropyLoss(ignore_index=vocab["<pad>"])
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    histories = []
    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        for src, tgt in train_loader:
            optimizer.zero_grad()
            logits = model(src, tgt)
            loss = criterion(logits.reshape(-1, len(vocab)), tgt[:, 1:].reshape(-1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        histories.append(total_loss / len(train_loader))
        if (epoch + 1) % 20 == 0 or epoch == 0:
            print(f"epoch {epoch + 1}/{epochs} loss={histories[-1]:.4f}")
    return histories


lstm_model = LSTMSeq2Seq(len(vocab), EMBED_DIM, HIDDEN_SIZE)
transformer_model = TransformerSeq2Seq(len(vocab), EMBED_DIM, HIDDEN_SIZE, MAX_LEN)

print("Training LSTM Seq2Seq")
train_model(lstm_model, EPOCHS)
print("Training Transformer Seq2Seq")
train_model(transformer_model, EPOCHS)

samples = [
    "How do I change my email?",
    "My order is delayed",
    "Can I cancel my subscription?",
    "Where do I find my invoice?",
]

for sample in samples:
    src = torch.tensor([encode_sequence(sample, vocab)], dtype=torch.long)
    lstm_tokens = lstm_model.predict(src[0])
    transformer_tokens = transformer_model.predict(src[0])
    print(f"Input: {sample}")
    print(f"LSTM: {decode_tokens(lstm_tokens)}")
    print(f"Transformer: {decode_tokens(transformer_tokens)}")
    print("---")
