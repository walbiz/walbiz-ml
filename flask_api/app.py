from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

from franchise_cosine import franchise_recommendations

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    input_data = data['input_data']
    recommendations = franchise_recommendations(input_data)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)