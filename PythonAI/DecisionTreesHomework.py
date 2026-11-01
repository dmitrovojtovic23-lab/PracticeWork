from importlib.util import find_spec
import sys
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, r2_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
def print_table(headers, rows):
    widths = [len(str(header)) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))
    print(" | ".join(str(header).ljust(widths[index]) for index, header in enumerate(headers)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)))
def print_regression_result(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    score = r2_score(y_test, model.predict(X_test))
    print_table(["Модель", "R2 на тестовій вибірці"], [[name, f"{score:.4f}"]])
    return score
def task1(X_train, X_test, y_train, y_test):
    print("Завдання 1")
    model = DecisionTreeRegressor(max_depth=4, random_state=42)
    print_regression_result("DecisionTreeRegressor", model, X_train, X_test, y_train, y_test)
def task2(X_train, X_test, y_train, y_test):
    print("\nЗавдання 2")
    models = [
        ("DecisionTreeRegressor", DecisionTreeRegressor(max_depth=4, random_state=42)),
        ("RandomForestRegressor", RandomForestRegressor(n_estimators=100, random_state=42)),
    ]
    rows = []
    for name, model in models:
        model.fit(X_train, y_train)
        score = r2_score(y_test, model.predict(X_test))
        rows.append([name, f"{score:.4f}"])
    print_table(["Модель", "R2 на тестовій вибірці"], rows)
    return dict(zip((name for name, _ in models), (float(row[1]) for row in rows)))
def task3(X_train, X_test, y_train, y_test, forest_score):
    print("\nЗавдання 3")
    if find_spec("xgboost") is not None:
        
        model = XGBRegressor(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
        )
        model_name = "XGBRegressor"
    else:
        model = GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
        )
        model_name = "GradientBoostingRegressor (заміна: xgboost не встановлено)"
    model.fit(X_train, y_train)
    score = r2_score(y_test, model.predict(X_test))
    print_table(
        ["Модель", "R2 на тестовій вибірці"],
        [
            [model_name, f"{score:.4f}"],
            ["RandomForestRegressor", f"{forest_score:.4f}"],
        ],
    )
def task4(X_train, X_test, y_train, y_test, median_price):
    print("\nЗавдання 4")
    y_train_class = (y_train > median_price).astype(int)
    y_test_class = (y_test > median_price).astype(int)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train_class)
    predictions = model.predict(X_test)
    matrix = confusion_matrix(y_test_class, predictions, labels=[0, 1])

    print("Confusion matrix (рядки — фактичний клас, стовпці — передбачений)")
    print_table(["Фактичний клас", "Передбачено 0", "Передбачено 1"], [
        [0, matrix[0, 0], matrix[0, 1]],
        [1, matrix[1, 0], matrix[1, 1]],
    ])
    print_table(["Метрика", "Значення"], [
        ["Accuracy", f"{accuracy_score(y_test_class, predictions):.4f}"],
        ["Precision", f"{precision_score(y_test_class, predictions, zero_division=0):.4f}"],
        ["Recall", f"{recall_score(y_test_class, predictions, zero_division=0):.4f}"],
        ["F1", f"{f1_score(y_test_class, predictions, zero_division=0):.4f}"],
    ])
def main():
    sys.stdout.reconfigure(encoding="utf-8")
    housing = fetch_california_housing()
    feature_names = ["MedInc", "HouseAge", "AveRooms", "AveBedrms"]
    feature_indices = [housing.feature_names.index(name) for name in feature_names]
    X = housing.data[:, feature_indices]
    y = housing.target
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )
    task1(X_train, X_test, y_train, y_test)
    forest_scores = task2(X_train, X_test, y_train, y_test)
    task3(X_train, X_test, y_train, y_test, forest_scores["RandomForestRegressor"])
    task4(X_train, X_test, y_train, y_test, float(np.median(y)))
if __name__ == "__main__":
    main()