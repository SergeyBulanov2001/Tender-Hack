from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import configuration


app = Flask(__name__)

app.config.from_object(configuration.Configuration())

db = SQLAlchemy(app)
