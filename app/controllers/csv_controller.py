from flask import Flask, json, Response
from app.utils import read_csv, format_csv_data

app = Flask(__name__)

@app.route('/franchises', methods=['GET'])
def display_csv():
    csv_data = read_csv('./app/dataset/franchise_walbiz.csv')
    formatted_data = format_csv_data(csv_data)
    json_data = json.dumps(formatted_data, indent=2, sort_keys=False)
    return Response(json_data, content_type='application/json')
