import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def main():
    data = load_diabetes()
    X = data.data[:, 2:3]
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print("Перші 10 реальних і передбачених значень:")
    for actual, predicted in zip(y_test[:10], predictions[:10]):
        print(f"{actual:.2f} | {predicted:.2f}")

    x_min = float(X.min())
    x_max = float(X.max())
    line_x = [x_min, x_max]
    line_y = [model.intercept_ + model.coef_[0] * x_min, model.intercept_ + model.coef_[0] * x_max]

    plt.figure(figsize=(10, 6))
    plt.scatter(X_train, y_train, color="blue", alpha=0.6, label="Навчальні дані")
    plt.scatter(X_test, y_test, color="green", alpha=0.6, label="Тестові дані")
    plt.plot(line_x, line_y, color="red", linewidth=2, label="Лінія регресії")
    plt.title("Лінійна регресія на датасеті diabetes")
    plt.xlabel("X — значення ознаки")
    plt.ylabel("Y — реальне значення цільової змінної")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("AssignmentsPractice.png")

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, predictions, color="purple", alpha=0.8)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="black", linestyle="--", linewidth=1)
    plt.title("Реальні vs передбачені значення")
    plt.xlabel("Реальне значення")
    plt.ylabel("Передбачене значення")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("AssignmentsPracticePredictions.png")


if __name__ == "__main__":
    main()
