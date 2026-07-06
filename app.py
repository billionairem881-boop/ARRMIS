from flask import Flask
from flask_login import LoginManager
from config import Config

from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

# ===============================
# DATABASE
# ===============================

db.init_app(app)

# ===============================
# LOGIN MANAGER
# ===============================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please log in first."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ===============================
# IMPORT ROUTES
# ===============================

import routes


# ===============================
# CREATE DATABASE TABLES
# ===============================

with app.app_context():
    db.create_all()


# ===============================
# RUN APPLICATION
# ===============================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )