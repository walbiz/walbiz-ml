from flask import Flask, json, Response
from app.utils import read_csv, format_csv_data, find_row_by_id
from app import app


@app.route('/franchises', methods=['GET'])
def display_csv():
    csv_data = read_csv('./app/dataset/franchise_walbiz.csv')
    formatted_data = format_csv_data(csv_data)
    json_data = json.dumps(formatted_data, indent=2, sort_keys=False)
    return Response(json_data, content_type='application/json')

@app.route('/franchises/<int:franchise_id>', methods=['GET'])
def display_single_csv(franchise_id):
    csv_data = read_csv('./app/dataset/franchise_walbiz.csv')
    selected_row = find_row_by_id(csv_data, franchise_id)

    if selected_row:
        formatted_row = {
            "id": selected_row["franchise_id"],
            "name": selected_row["franchise_name"],
            "type": selected_row["franchise_type"],
            "category": selected_row["franchise_category"],
            "costs": selected_row["costs"],
            "logoImageUrl": selected_row["franchise_href"],
        }
        json_data = json.dumps(formatted_row, indent=2, sort_keys=False) 
        return Response(json_data, content_type='application/json')
    else:
        return Response(json.dumps({'error': 'Franchise ID not found'}), content_type='application/json'), 404
