from app import app
from models import db

def initialize_database():
    with app.app_context():
        db.create_all()
        print("=" * 50)
        print("ARRMIS Database Initialized Successfully!")
        print("All tables have been created.")
        print("=" * 50)

if __name__ == "__main__":
    initialize_database()