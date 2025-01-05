from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Получаем данные из запроса
    data = request.json
    input_value = data.get('input', 0)
    
    # Простая логика для примера
    result = {"output": input_value * 2}
    return jsonify(result)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Python server is running"})

if __name__ == '__main__':
    port = int(os.getenv('PYTHON_PORT', 6444))
    app.run(host='0.0.0.0', port=port)
