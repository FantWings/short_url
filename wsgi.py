from flask import Flask
from flask_cors import CORS

from settings import FlaskConfig
from sql.model import db
from routes.index import index
from routes.url import url
from routes.auth import auth

app = Flask(__name__)
app.config.from_object(FlaskConfig)

with app.app_context():
    db.init_app(app)
    db.create_all()

CORS(app)
app.register_blueprint(blueprint=index, url_prefix='/')
app.register_blueprint(blueprint=url, url_prefix='/url')
app.register_blueprint(blueprint=auth, url_prefix='/auth')

if __name__ == "__main__":
    app.run()
