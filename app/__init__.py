from flask import Flask

app = Flask(__name__)

# Import modul untuk mendeklarasikan route atau konfigurasi lainnya
from app.controllers import controller
