from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    result = {"prediction": data["input"] * 2}  # Пример обработки
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=6000)