import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def print_table(headers, rows):
    widths = [len(str(header)) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    border = "-+-".join("-" * width for width in widths)
    header_line = " | ".join(str(header).ljust(widths[index]) for index, header in enumerate(headers))
    print(header_line)
    print(border)
    for row in rows:
        print(" | ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)))


def fit_linear_regression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    score = r2_score(y_test, predictions)
    return X_train, X_test, y_train, y_test, model, predictions, score


def task1():
    housing = fetch_california_housing()
    X = housing.data[:, [0]]
    y = housing.target
    _, _, _, _, _, _, score = fit_linear_regression(X, y)

    print("Завдання 1")
    print_table(["Модель", "Ознаки", "R^2"], [["LinearRegression", "MedInc", f"{score:.4f}"]])

    housing = fetch_california_housing()
    X = housing.data[:, [0]]
    y = housing.target
    X_train, X_test, y_train, y_test, model, _, _ = fit_linear_regression(X, y)

    x_min = float(X.min())
    x_max = float(X.max())
    line_x = [x_min, x_max]
    slope = float(model.coef_[0])
    line_y = [model.intercept_ + slope * x_min, model.intercept_ + slope * x_max]

    plt.figure(figsize=(10, 6))
    plt.scatter(X_train, y_train, color="blue", alpha=0.5, label="Навчальні дані")
    plt.scatter(X_test, y_test, color="green", alpha=0.5, label="Тестові дані")
    plt.plot(line_x, line_y, color="red", linewidth=2, label="Лінія регресії")
    plt.title("Лінійна регресія для MedInc")
    plt.xlabel("MedInc")
    plt.ylabel("Median House Value")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("task1.png")
    plt.close()


def task2():
    housing = fetch_california_housing()
    rng = np.random.RandomState(42)
    selected = rng.choice(len(housing.target), size=5000, replace=False)
    X_sample = housing.data[selected]
    y_sample = housing.target[selected]

    print("\nЗавдання 2")
    rows = []
    feature_sets = {
        "MedInc": [0],
        "MedInc, AveRooms": [0, 2],
    }

    for name, indices in feature_sets.items():
        X = X_sample[:, indices]
        _, _, _, _, _, _, score = fit_linear_regression(X, y_sample)
        rows.append(["LinearRegression", name, f"{score:.4f}"])

    print_table(["Модель", "Ознаки", "R^2"], rows)


def task3():
    housing = fetch_california_housing()
    rng = np.random.RandomState(42)
    selected = rng.choice(len(housing.target), size=5000, replace=False)
    X = housing.data[selected][:, [0, 2]]
    y = housing.target[selected]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = math.sqrt(mse)
    score = r2_score(y_test, predictions)

    print("\nЗавдання 3")
    print_table(["Метрика", "Значення"], [
        ["MAE", f"{mae:.4f}"],
        ["MSE", f"{mse:.4f}"],
        ["RMSE", f"{rmse:.4f}"],
        ["R^2", f"{score:.4f}"],
    ])

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, predictions, color="purple", alpha=0.7)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="black", linestyle="--", linewidth=1, label="y=x")
    plt.title("Реальні vs передбачені значення")
    plt.xlabel("Реальні значення")
    plt.ylabel("Передбачені значення")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("task3.png")
    plt.close()


def task4():
    housing = fetch_california_housing()
    X = housing.data[:, [0, 2]]
    y = housing.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("\nЗавдання 4")
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, predictions, color="purple", alpha=0.7)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="black", linestyle="--", linewidth=1, label="y=x")
    plt.title("Реальні vs передбачені значення")
    plt.xlabel("Реальне значення")
    plt.ylabel("Передбачене значення")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("task4.png")
    plt.close()


def main():
    task1()
    task2()
    task3()
    task4()


if __name__ == "__main__":
    main()
