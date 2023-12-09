from flask import Flask
from app.controllers.controller import display_csv, display_single_csv

app = Flask(__name__)

app.add_url_rule('/franchises', 'display_csv', display_csv)
app.add_url_rule('/franchises/<int:franchise_id>', 'display_single_csv', display_single_csv)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
