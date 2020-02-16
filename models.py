from app import db


class TableFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(13), unique=True, nullable=False)
