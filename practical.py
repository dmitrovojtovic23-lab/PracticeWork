import numpy as np
import torch
from sklearn.datasets import make_regression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn


def set_seed(seed=42):
    np.random.seed(seed)
    torch.manual_seed(seed)


def make_data():
    X, y = make_regression(n_samples=200, n_features=10, noise=10, random_state=42)
    X = X.astype(np.float32)
    y = y.astype(np.float32)
    return X, y


def print_table(headers, rows):
    widths = [len(str(header)) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))
    separator = "-+-".join("-" * width for width in widths)
    print(" | ".join(str(header).ljust(widths[index]) for index, header in enumerate(headers)))
    print(separator)
    for row in rows:
        print(" | ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)))


def activate(name):
    if name == "ReLU":
        return nn.ReLU()
    if name == "Tanh":
        return nn.Tanh()
    if name == "LeakyReLU":
        return nn.LeakyReLU(0.01)
    if name == "Swish":
        return nn.SiLU()
    raise ValueError(f"Unknown activation: {name}")


def build_model(activation_name, dropout=0.0, batch_norm=False):
    layers = []
    in_features = 10
    hidden_sizes = [64, 32]
    for hidden_size in hidden_sizes:
        layers.append(nn.Linear(in_features, hidden_size))
        if batch_norm:
            layers.append(nn.BatchNorm1d(hidden_size))
        layers.append(activate(activation_name))
        if dropout > 0:
            layers.append(nn.Dropout(dropout))
        in_features = hidden_size
    layers.append(nn.Linear(in_features, 1))
    return nn.Sequential(*layers)


def train_model(model, X_train, y_train, X_val, y_val, epochs=300, lr=0.01):
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    best_state = None
    best_loss = float("inf")
    for _ in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train).squeeze(1)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            val_pred = model(X_val).squeeze(1)
            val_loss = criterion(val_pred, y_val).item()
        if val_loss < best_loss:
            best_loss = val_loss
            best_state = {key: value.clone() for key, value in model.state_dict().items()}
    if best_state is not None:
        model.load_state_dict(best_state)
    return model


def evaluate_model(model, X_test, y_test):
    model.eval()
    with torch.no_grad():
        predictions = model(X_test).squeeze(1).numpy().astype(np.float32)
    targets = y_test.numpy().astype(np.float32)
    mae = mean_absolute_error(targets, predictions)
    r2 = r2_score(targets, predictions)
    return mae, r2


def prepare_split():
    X, y = make_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = torch.tensor(scaler.fit_transform(X_train), dtype=torch.float32)
    X_test = torch.tensor(scaler.transform(X_test), dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32)
    return X_train, X_test, y_train, y_test


def task_1():
    print("Завдання 1")
    X_train, X_test, y_train, y_test = prepare_split()
    results = []
    for activation_name in ["ReLU", "Tanh", "LeakyReLU", "Swish"]:
        model = build_model(activation_name, dropout=0.0, batch_norm=False)
        model = train_model(model, X_train, y_train, X_test, y_test, epochs=300)
        mae, r2_value = evaluate_model(model, X_test, y_test)
        results.append([activation_name, f"{mae:.4f}", f"{r2_value:.4f}"])
    print_table(["Активація", "MAE", "R^2"], results)
    print()


def task_2():
    print("Завдання 2")
    X_train, X_test, y_train, y_test = prepare_split()
    model = build_model("ReLU", dropout=0.2, batch_norm=False)
    model = train_model(model, X_train, y_train, X_test, y_test, epochs=300)
    mae, r2_value = evaluate_model(model, X_test, y_test)
    print("Конфігурація: ReLU + Dropout")
    print(f"MAE: {mae:.4f}")
    print(f"R^2: {r2_value:.4f}")
    print()


def task_3():
    print("Завдання 3")
    X_train, X_test, y_train, y_test = prepare_split()
    model = build_model("ReLU", dropout=0.0, batch_norm=True)
    model = train_model(model, X_train, y_train, X_test, y_test, epochs=300)
    mae, r2_value = evaluate_model(model, X_test, y_test)
    print("Конфігурація: ReLU + BatchNorm")
    print(f"MAE: {mae:.4f}")
    print(f"R^2: {r2_value:.4f}")
    print()


def task_4():
    print("Завдання 4")
    X_train, X_test, y_train, y_test = prepare_split()
    configs = [
        ("ReLU", 0.0, False),
        ("ReLU", 0.2, False),
        ("ReLU", 0.0, True),
        ("ReLU", 0.2, True),
    ]
    results = []
    for activation_name, dropout, batch_norm in configs:
        model = build_model(activation_name, dropout=dropout, batch_norm=batch_norm)
        model = train_model(model, X_train, y_train, X_test, y_test, epochs=300)
        mae, r2_value = evaluate_model(model, X_test, y_test)
        label = activation_name
        if dropout > 0:
            label += " + Dropout"
        if batch_norm:
            label += " + BatchNorm"
        results.append([label, f"{mae:.4f}", f"{r2_value:.4f}"])
    print_table(["Конфігурація", "MAE", "R^2"], results)
    best = max(results, key=lambda row: float(row[2]))
    print(f"Найкраща конфігурація: {best[0]} (R^2 = {best[2]})")
    print()


def main():
    set_seed(42)
    task_1()
    task_2()
    task_3()
    task_4()


if __name__ == "__main__":
    main()
