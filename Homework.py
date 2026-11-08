import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
diabetes = load_diabetes()
X, y = diabetes.data, diabetes.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")
X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
X_test_t = torch.tensor(X_test, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)
class MLPRegressor(nn.Module):
    def __init__(self, input_dim):
        super(MLPRegressor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
    def forward(self, x):
        return self.network(x)
def train_and_evaluate(weight_decay_val=0.0):
    torch.manual_seed(42)
    model = MLPRegressor(X_train.shape[1])
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=weight_decay_val)
    dataset = TensorDataset(X_train_t, y_train_t)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    for epoch in range(50):
        model.train()
        for batch_x, batch_y in loader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
    model.eval()
    with torch.no_grad():
        predictions = model(X_test_t).numpy()
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return mae, r2, predictions
mae_no_reg, r2_no_reg, pred_no_reg = train_and_evaluate(weight_decay_val=0.0)
mae_l2, r2_l2, pred_l2 = train_and_evaluate(weight_decay_val=1e-4)
print("\n" + "="*50)
print(f"{'Конфігурація':<25} | {'MAE':<10} | {'R2':<10}")
print("-"*50)
print(f"{'Без регуляризації':<25} | {mae_no_reg::<10.4f} | {r2_no_reg::<10.4f}")
print(f"{'З регуляризацією (L2)':<25} | {mae_l2::<10.4f} | {r2_l2::<10.4f}")
print("="*50 + "\n")
plt.figure(figsize=(8, 6))
plt.scatter(y_test, pred_no_reg, color='blue', alpha=0.6, label='Без регуляризації')
plt.scatter(y_test, pred_l2, color='green', alpha=0.6, label='З регуляризацією (L2)')
ideal_line = np.linspace(min(y_test), max(y_test), 100)
plt.plot(ideal_line, ideal_line, color='red', linestyle='--', label='Ідеальні передбачення (y = x)')
plt.xlabel('Реальні значення (y_test)')
plt.ylabel('Передбачені значення (y_pred)')
plt.title('Порівняння реальних та передбачених значень цільової змінної')
plt.legend()
plt.grid(True)
plt.savefig('diabetes_healthrisk_analysis.png')
plt.show()
 