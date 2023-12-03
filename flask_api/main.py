from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recomendation', methods=['GET'])
def get_csv_data():
    csv_data = read_csv('export_walbiz.csv')
    return jsonify({'csv_data': csv_data})

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
    return data

if __name__ == "__main__":
    app.run(debug=True)