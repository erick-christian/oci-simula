import os
from app import app, db, Usuario
from sqlalchemy import text

with app.app_context():


    # Attempt to create the new tables (Usuario)
    db.create_all()
    print("Created tables.")

    # Insert default admin user if not exists
    admin = Usuario.query.filter_by(correo='admin@oci.com').first()
    if not admin:
        admin = Usuario(correo='admin@oci.com')
        admin.set_password('oci2026')
        db.session.add(admin)
        db.session.commit()
        print("Created default admin user: admin@oci.com")
    else:
        print("Admin user already exists.")
