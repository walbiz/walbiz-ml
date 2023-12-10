from flask import Flask
from app.controllers.csv_controller import display_csv
from app.controllers.single_csv_controller import display_single_csv
from app.controllers.discover_controller import recommend
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

app.add_url_rule('/franchises', 'display_csv', display_csv)
app.add_url_rule('/franchises/<int:franchise_id>', 'display_single_csv', display_single_csv)
app.add_url_rule('/franchises/discover', 'recommend', recommend)

if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()
