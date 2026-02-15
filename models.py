from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Mensaje {self.id}>'
