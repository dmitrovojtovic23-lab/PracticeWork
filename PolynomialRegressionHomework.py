from sklearn.datasets import fetch_california_housing
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
housing = fetch_california_housing()
feature_names = housing.feature_names
medinc_idx = feature_names.index("MedInc")
X_medinc = housing.data[:, [medinc_idx]]
target_features = ["MedInc", "HouseAge", "AveRooms", "AveBedrms"]
target_indices = [feature_names.index(f) for f in target_features]
X_multi = housing.data[:, target_indices]
y = housing.target
print("=== Завдання 1 та 2: Поліноміальна регресія ===")
results_poly = []
for degree in range(1, 4):
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X_medinc)
    X_train, X_test, y_train, y_test = train_test_split(
        X_poly, y, test_size=0.20, random_state=42
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    r2_train = r2_score(y_train, model.predict(X_train))
    r2_test = r2_score(y_test, model.predict(X_test))
    results_poly.append({
        "Ступінь полінома": degree,
        "R² поїзд": round(r2_train, 4),
        "Тест R²": round(r2_test, 4)
    })
df_poly = pd.DataFrame(results_poly)
print(df_poly.to_string(index=False))
print("\n" + "="*50 + "\n")
print("=== Завдання 3: Lasso-регуляризація ===")
X_train, X_test, y_train, y_test = train_test_split(
    X_multi, y, test_size=0.20, random_state=42
)
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_r2 = r2_score(y_test, lr_model.predict(X_test))
lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)
lasso_r2 = r2_score(y_test, lasso_model.predict(X_test))
zero_coefs_lasso = np.sum(lasso_model.coef_ == 0)
print(f"LinearRegression Тест R²: {round(lr_r2, 4)}")
print(f"Lasso(alpha=0.1) Тест R²: {round(lasso_r2, 4)}")
print(f"Коефіцієнти LinearRegression: {lr_model.coef_}")
print(f"Коефіцієнти Lasso: {lasso_model.coef_}")
print(f"Кількість коефіцієнтів, що стали рівними 0 у Lasso: {zero_coefs_lasso}")
print("\n" + "="*50 + "\n")
print("=== Завдання 4: Ridge-регуляризація ===")
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
ridge_r2 = r2_score(y_test, ridge_model.predict(X_test))
lr_non_zero = np.sum(lr_model.coef_ != 0)
ridge_non_zero = np.sum(ridge_model.coef_ != 0)
results_ridge = [
    {
        "Модель": "LinearRegression",
        "Тест R²": round(lr_r2, 4),
        "Кількість ненульових коеф.": lr_non_zero
    },
    {
        "Модель": "Хребет(альфа=1.0)",
        "Тест R²": round(ridge_r2, 4),
        "Кількість ненульових коеф.": ridge_non_zero
    }
]
df_ridge = pd.DataFrame(results_ridge)
print(df_ridge.to_string(index=False))
 