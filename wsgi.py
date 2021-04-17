from flask import Flask
from flask_cors import CORS

from config import Config
from sql.model import db
from routes.index import index
# from routes.api import api
# from routes.auth import auth

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    db.init_app(app)
    db.create_all()

CORS(app)
app.register_blueprint(blueprint=index, url_prefix='/')
# app.register_blueprint(blueprint=api, url_prefix='/api')
# app.register_blueprint(blueprint=auth, url_prefix='/auth')

if __name__ == "__main__":
    app.run()
