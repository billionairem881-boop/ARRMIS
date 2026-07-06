from app import app, db
from models import User

with app.app_context():

    username = "admin"

    existing = User.query.filter_by(username=username).first()

    if existing:
        print("Admin account already exists.")

    else:
        admin = User(
            username="admin",
            full_name="System Administrator",
            email="admin@arrmis.com",
            role="admin",
            active=True
        )

        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("=" * 50)
        print("ARRMIS Administrator Created Successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("=" * 50)