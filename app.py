from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import configuration

UPLOAD_FOLDER = 'data/files'


app = Flask(__name__)

app.config.from_object(configuration.Configuration())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
