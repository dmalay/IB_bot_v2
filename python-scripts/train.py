import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Загружаем данные (примерный файл data/dataset.csv)
data = pd.read_csv('data/dataset.csv')

# Разделяем данные на признаки (X) и целевую переменную (y)
X = data[['feature1', 'feature2']]  # Замените на реальные имена колонок
y = data['target']

# Разделяем данные на тренировочные и тестовые наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Инициализация и обучение модели
model = LinearRegression()
model.fit(X_train, y_train)

# Оценка модели
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Сохранение модели в файл
joblib.dump(model, 'models/linear_regression_model.pkl')
print("Model saved to models/linear_regression_model.pkl")
