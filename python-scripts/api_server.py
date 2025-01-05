from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import joblib
import numpy as np

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)

# Загрузка модели
model = joblib.load('models/linear_regression_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Получаем данные из запроса
    data = request.json
    features = data.get('features', [])
    
    if not features or len(features) == 0:
        return jsonify({"error": "Features are missing"}), 400
    
    try:
        features = np.array(features).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({"prediction": prediction[0]})  # response format  {"prediction": 6.4}

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Python server is running"})

if __name__ == '__main__':
    port = int(os.getenv('PYTHON_PORT', 6444))
    app.run(host='0.0.0.0', port=port)
