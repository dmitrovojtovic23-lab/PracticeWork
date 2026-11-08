import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.datasets import fetch_openml
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn


def print_table(headers, rows):
    widths = [len(str(header)) for header in headers]
    for row in rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len(str(value)))
    separator = "-+-".join("-" * width for width in widths)
    print(" | ".join(str(header).ljust(widths[idx]) for idx, header in enumerate(headers)))
    print(separator)
    for row in rows:
        print(" | ".join(str(value).ljust(widths[idx]) for idx, value in enumerate(row)))


def load_data():
    try:
        X, y = fetch_openml("heart-disease", version=1, return_X_y=True, as_frame=True)
        X = X.to_numpy(dtype=np.float32)
        y = y.to_numpy(dtype=np.float32)
    except Exception:
        from sklearn.datasets import load_breast_cancer

        dataset = load_breast_cancer()
        X = dataset.data.astype(np.float32)
        y = dataset.target.astype(np.float32)
    return X, y


class MLPClassifier(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.network(x)


def main():
    np.random.seed(42)
    torch.manual_seed(42)

    X, y = load_data()
    y = y.reshape(-1)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    dataset = torch.utils.data.TensorDataset(X_train_tensor, y_train_tensor)
    loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

    model = MLPClassifier(X_train.shape[1])
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    train_loss = []
    train_accuracy = []

    for epoch in range(1, 31):
        model.train()
        running_loss = 0.0
        for batch_X, batch_y in loader:
            optimizer.zero_grad()
            outputs = model(batch_X).squeeze(1)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * batch_X.size(0)

        avg_loss = running_loss / len(X_train_tensor)
        model.eval()
        with torch.no_grad():
            train_probs = model(X_train_tensor).squeeze(1)
            train_predictions = (train_probs >= 0.5).float()
            acc = accuracy_score(y_train_tensor.numpy(), train_predictions.numpy())

        train_loss.append(avg_loss)
        train_accuracy.append(acc)
        print(f"Епоха {epoch:02d} | Loss: {avg_loss:.4f} | Accuracy: {acc:.4f}")

    model.eval()
    with torch.no_grad():
        test_probs = model(X_test_tensor).squeeze(1)
        test_predictions = (test_probs >= 0.5).float()
        final_loss = criterion(test_probs, y_test_tensor).item()
        final_accuracy = accuracy_score(y_test_tensor.numpy(), test_predictions.numpy())
        final_precision = precision_score(y_test_tensor.numpy(), test_predictions.numpy(), zero_division=0)
        final_recall = recall_score(y_test_tensor.numpy(), test_predictions.numpy(), zero_division=0)
        final_f1 = f1_score(y_test_tensor.numpy(), test_predictions.numpy(), zero_division=0)
        cm = confusion_matrix(y_test_tensor.numpy(), test_predictions.numpy(), labels=[0, 1])

    print()
    print_table(["Метрика", "Значення"], [
        ["Loss", f"{final_loss:.4f}"],
        ["Accuracy", f"{final_accuracy:.4f}"],
        ["Precision", f"{final_precision:.4f}"],
        ["Recall", f"{final_recall:.4f}"],
        ["F1", f"{final_f1:.4f}"],
    ])
    print()
    print_table(["Фактичний клас", "Передбачено 0", "Передбачено 1"], [
        [0, int(cm[0, 0]), int(cm[0, 1])],
        [1, int(cm[1, 0]), int(cm[1, 1])],
    ])

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 31), train_loss, color="tab:blue", marker="o", linewidth=2)
    plt.title("Loss за епохами")
    plt.xlabel("Епоха")
    plt.ylabel("Loss")
    plt.grid(True, alpha=0.3)
    plt.legend(["Loss"])
    plt.tight_layout()
    plt.savefig("loss_healthrisk_mlp.png")

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 31), train_accuracy, color="tab:green", marker="o", linewidth=2)
    plt.title("Accuracy за епохами")
    plt.xlabel("Епоха")
    plt.ylabel("Accuracy")
    plt.grid(True, alpha=0.3)
    plt.legend(["Accuracy"])
    plt.tight_layout()
    plt.savefig("accuracy_healthrisk_mlp.png")

    print()
    if final_accuracy >= 0.8:
        conclusion = "Модель покращує якість на тестовій вибірці, і точність досягає високого рівня."
    elif final_accuracy >= 0.7:
        conclusion = "Модель показує прийнятну якість, але ще може бути покращена."
    else:
        conclusion = "Модель має низьку точність і потребує покращення архітектури або підбору гіперпараметрів."
    print(f"Висновок: {conclusion}")


if __name__ == "__main__":
    main()
