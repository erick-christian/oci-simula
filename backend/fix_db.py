import os
from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE reactivos ADD COLUMN imagen_url VARCHAR(255);"))
        db.session.commit()
        print("Added imagen_url column to reactivos table.")
    except Exception as e:
        db.session.rollback()
        print("Column imagen_url might already exist or error occurred:", e)
