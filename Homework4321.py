import argparse
import os
import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from torchvision.models import ResNet18_Weights

SEED = 42


def set_seed():
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)


def ensure_dataset(data_dir):
    path = Path(data_dir)
    if path.exists():
        return str(path)
    try:
        import kagglehub

        dataset_path = kagglehub.dataset_download("paultimothymooney/chest-xray-pneumonia")
        if os.path.exists(dataset_path):
            return dataset_path
    except Exception:
        pass
    raise FileNotFoundError(
        "Dataset not found. Please download the Chest X-Ray Pneumonia dataset and set --data-dir to the dataset folder."
    )


def build_loaders(data_dir, batch_size=32):
    image_size = 224
    transform = transforms.Compose(
        [
            transforms.Grayscale(num_output_channels=3),
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    dataset_dir = Path(data_dir)
    train_dir = dataset_dir / "train"
    val_dir = dataset_dir / "val"
    if not (train_dir.exists() and val_dir.exists()):
        dataset_dir = dataset_dir / "chest_xray"
        train_dir = dataset_dir / "train"
        val_dir = dataset_dir / "val"

    if not (train_dir.exists() and val_dir.exists()):
        raise FileNotFoundError(f"Expected dataset folders: {train_dir} and {val_dir}")

    train_dataset = datasets.ImageFolder(str(train_dir), transform=transform)
    val_dataset = datasets.ImageFolder(str(val_dir), transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    return train_loader, val_loader, train_dataset, val_dataset


def build_model():
    model = models.resnet18(weights=ResNet18_Weights.DEFAULT)
    for param in model.parameters():
        param.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, 2)
    return model


def compute_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    return acc, precision, recall, f1, cm


def save_prediction_plot(model, val_loader, device, output_path, class_names):
    model.eval()
    selected = []
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            preds = outputs.argmax(dim=1).cpu().numpy()
            labels = labels.cpu().numpy()
            for idx in range(inputs.size(0)):
                selected.append({
                    "image": inputs[idx].cpu(),
                    "true": labels[idx],
                    "pred": int(preds[idx]),
                })
                if len(selected) >= 8:
                    break
            if len(selected) >= 8:
                break

    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    axes = axes.flatten()
    for ax, sample in zip(axes, selected):
        image = sample["image"].permute(1, 2, 0).numpy()
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        image = image * std + mean
        image = np.clip(image, 0, 1)
        ax.imshow(image)
        ax.set_title(f"T: {class_names[sample['true']]}, P: {class_names[sample['pred']]}")
        ax.axis("off")

    for ax in axes[len(selected):]:
        ax.axis("off")

    fig.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close(fig)


def train(model, train_loader, val_loader, device, epochs=5):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-4)
    best_state = None
    best_val_loss = float("inf")

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for inputs, targets in train_loader:
            inputs = inputs.to(device)
            targets = targets.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        model.eval()
        val_loss = 0.0
        all_preds = []
        all_true = []
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs = inputs.to(device)
                targets = targets.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                val_loss += loss.item()
                preds = outputs.argmax(dim=1)
                all_preds.extend(preds.cpu().tolist())
                all_true.extend(targets.cpu().tolist())

        avg_loss = running_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        print(f"Epoch {epoch + 1}/{epochs} - Train loss: {avg_loss:.4f} - Val loss: {avg_val_loss:.4f}")
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        acc, precision, recall, f1, cm = compute_metrics(all_true, all_preds)
        print(f"Accuracy: {acc:.4f} | Precision: {precision:.4f} | Recall: {recall:.4f} | F1: {f1:.4f}")
        print("Confusion matrix:")
        print(cm)

    if best_state is not None:
        model.load_state_dict(best_state)

    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default="./chest_xray", help="Path to the Chest X-Ray Pneumonia dataset")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=5)
    args = parser.parse_args()

    set_seed()

    data_dir = ensure_dataset(args.data_dir)
    train_loader, val_loader, _, val_dataset = build_loaders(data_dir, batch_size=args.batch_size)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_model().to(device)

    model = train(model, train_loader, val_loader, device, epochs=args.epochs)

    model.eval()
    all_preds = []
    all_true = []
    with torch.no_grad():
        for inputs, targets in val_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            preds = outputs.argmax(dim=1)
            all_preds.extend(preds.cpu().tolist())
            all_true.extend(targets.tolist())

    acc, precision, recall, f1, cm = compute_metrics(all_true, all_preds)
    print("\nFinal evaluation")
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 score: {f1:.4f}")
    print("Confusion matrix:")
    print(cm)

    class_names = list(val_dataset.classes)
    save_prediction_plot(model, val_loader, device, "pneumonia_predictions.png", class_names)
    torch.save(model.state_dict(), "pneumonia_resnet18.pth")
    print("Model saved to pneumonia_resnet18.pth")
    print("Prediction plot saved to pneumonia_predictions.png")

    if f1 >= 0.8:
        readiness = "готова до впровадження"
    elif f1 >= 0.6:
        readiness = "частково готова, потрібне доопрацювання"
    else:
        readiness = "ще не готова до впровадження"
    print(f"Модель {readiness}. F1-score = {f1:.4f}")


if __name__ == "__main__":
    main()
