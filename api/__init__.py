from flask import Flask
from config import Config
from flask_sqlalchemy import SQLALchemy
from flask_migrate import Migrate 

app = Flask(__name__)
app.config.from_object(Config)
db = SQLALchemy(app)
migrate = Migrate(app, db)

from app import routes, models