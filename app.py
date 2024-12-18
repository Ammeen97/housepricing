from flask import Flask, request, jsonify, render_template
import pandas as pd
import time
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Queue
from threading import Thread
from producer_consumer import producer, consumer, stop_event

app = Flask(__name__)

# Define the make_prediction function
def make_prediction(input_data):
    file_choice = input_data.get("file", "train")
    if file_choice == "train":
        data = pd.read_csv('train.csv')
    elif file_choice == "test":
        data = pd.read_csv('test.csv')
    elif file_choice == "submission":
        data = pd.read_csv('submission.csv')
    else:
        return {"error": "Invalid file choice. Options are 'train', 'test', or 'submission'."}

    if 'SalePrice' in data.columns:
        avg_price = data['SalePrice'].mean()
        return {"average_price": avg_price, "file_used": file_choice}
    else:
        return {"message": f"The column 'SalePrice' is not available in the {file_choice} file."}

# Serve the HTML frontend
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    result = make_prediction(input_data)
    return jsonify(result)

# Get Submission Data
@app.route('/get_submission_data', methods=['GET'])
def get_submission_data():
    submission_data = pd.read_csv('submission.csv')
    return submission_data.to_json(orient='records')

# Get Test Data
@app.route('/get_test_data', methods=['GET'])
def get_test_data():
    test_data = pd.read_csv('test.csv')
    return test_data.to_json(orient='records')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

