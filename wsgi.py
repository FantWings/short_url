from flask import Flask
from flask_cors import CORS

from config import Config
from sql.mysql import db
from api.main import main

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

CORS(app)
app.register_blueprint(blueprint=main, url_prefix='/')

if __name__ == "__main__":
    app.run()
