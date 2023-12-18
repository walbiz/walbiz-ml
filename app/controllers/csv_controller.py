from flask import Flask, json, Response, request
from app.utils import read_csv, format_csv_data

app = Flask(__name__)

def paginate_data(data, page=None, size=None, limit=None, offset=None):
    page = int(page) if page is not None else 1
    size = int(size) if size is not None else len(data)
    limit = int(limit) if limit is not None else size
    offset = int(offset) if offset is not None else 0

    start_index = (page - 1) * size + offset
    end_index = start_index + limit
    return data[start_index:end_index]

@app.route('/franchises', methods=['GET'])
def display_csv():
    csv_data = read_csv('./app/dataset/franchise_walbiz.csv')
    formatted_data = format_csv_data(csv_data)

    page = request.args.get('page')
    size = request.args.get('size')
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    paginated_data = paginate_data(formatted_data, page, size, limit, offset)

    json_data = json.dumps({'franchises': paginated_data}, indent=2, sort_keys=False)
    return Response(json_data, content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)
