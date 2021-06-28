import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)

SECRET_KEY = os.urandom(32)

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_BINDS'] = {
   'new' : os.getenv("SQLALCHEMY_DATABASE_URI")
}
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

from app.model import *
from app.login.views import login_blueprint
from app.timeline.views import timeline_blueprint

# register our blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(timeline_blueprint)