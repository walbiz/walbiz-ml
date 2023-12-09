import csv

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
    return data

def format_csv_data(csv_data):
    formatted_data = []
    for row in csv_data:
        formatted_row = {
            "id": row["franchise_id"],
            "name": row["franchise_name"],
            "type": row["franchise_type"],
            "category": row["franchise_category"],
            "costs": row["costs"],
            "logoImageUrl": row["franchise_href"],
        }
        formatted_data.append(formatted_row)
    return formatted_data

def find_row_by_id(csv_data, franchise_id):
    for row in csv_data:
        if int(row["franchise_id"]) == franchise_id:
            return row
    return None
