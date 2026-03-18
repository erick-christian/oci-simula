import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://oci_user:oci_password@db:5432/oci_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # PostgreSQL command to add columns if they bypass error if already exist
            db.session.execute(text("ALTER TABLE reactivos ADD COLUMN reportado BOOLEAN DEFAULT FALSE;"))
            db.session.execute(text("ALTER TABLE reactivos ADD COLUMN revisado BOOLEAN DEFAULT FALSE;"))
            db.session.commit()
            print("Migración de base de datos exitosa: Se agregaron las columnas 'reportado' y 'revisado'.")
        except Exception as e:
            db.session.rollback()
            print(f"La migración falló, probablemente las columnas ya existen. Error: {e}")

if __name__ == '__main__':
    migrate()
