import joblib
import numpy as np

# Загрузка обученной модели
model = joblib.load('models/linear_regression_model.pkl')

# Функция для предсказания
def predict(features):
    features = np.array(features).reshape(1, -1)  # Преобразуем в формат [[x1, x2, ...]]
    prediction = model.predict(features)
    return prediction[0]

# Пример использования
if __name__ == "__main__":
    test_features = [5.0, 3.2]  # Замените на реальные значения
    print(f"Prediction: {predict(test_features)}")
