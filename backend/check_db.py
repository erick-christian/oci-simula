import os
from app import app, db, Usuario

with app.app_context():
    admin = Usuario.query.filter_by(correo='admin@oci.com').first()
    if admin:
        print(f"Found admin user: {admin.correo}")
        # Test password
        is_valid = admin.check_password('oci2026')
        print(f"Password 'oci2026' valid: {is_valid}")
        print(f"Hash: {admin.password_hash}")
    else:
        print("Admin user NOT FOUND in database!")
