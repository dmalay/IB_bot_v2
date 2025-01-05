from sklearn.linear_model import LinearRegression
import numpy as np

# Данные
X = np.array([[1], [2], [3]])
y = np.array([2, 4, 6])

# Обучение
model = LinearRegression()
model.fit(X, y)

print("Model trained.")
