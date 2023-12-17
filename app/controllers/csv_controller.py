from flask import Flask, json, Response, request
from app.utils import read_csv, format_csv_data

app = Flask(__name__)

def paginate_data(data, limit, offset):
    return data[offset:offset + limit]

@app.route('/franchises', methods=['GET'])
def display_csv():
    csv_data = read_csv('./app/dataset/franchise_walbiz.csv')
    formatted_data = format_csv_data(csv_data)

    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    paginated_data = paginate_data(formatted_data, limit, offset)
    
    json_data = json.dumps({'franchises': paginated_data}, indent=2, sort_keys=False)
    return Response(json_data, content_type='application/json')
