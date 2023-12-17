from flask import Flask, json, Response, request
from app.utils import read_csv, format_csv_data

app = Flask(__name__)

def paginate_data(data, limit=None, offset=None):
    # Convert limit and offset to integers
    limit = int(limit) if limit is not None else None
    offset = int(offset) if offset is not None else None

    # Perform slicing only if both limit and offset are valid integers
    if limit is not None and offset is not None:
        return data[offset:offset + limit]
    elif limit is not None:
        return data[:limit]
    else:
        return data

@app.route('/franchises', methods=['GET'])
def display_csv():
    csv_data = read_csv('./app/dataset/franchise_walbiz.csv')
    formatted_data = format_csv_data(csv_data)

    limit = request.args.get('limit')
    offset = request.args.get('offset')

    paginated_data = paginate_data(formatted_data, limit, offset)
    
    json_data = json.dumps({'franchises': paginated_data}, indent=2, sort_keys=False)
    return Response(json_data, content_type='application/json')
