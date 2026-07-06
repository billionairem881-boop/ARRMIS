import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ==========================================
    # FLASK SETTINGS
    # ==========================================
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "arrmis-secret-key"
    )

    # ==========================================
    # DATABASE
    # ==========================================
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "arrmis.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==========================================
    # FILE UPLOADS
    # ==========================================
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB

    # ==========================================
    # SESSION
    # ==========================================
    SESSION_PERMANENT = False

    SESSION_TYPE = "filesystem"

    # ==========================================
    # APPLICATION
    # ==========================================
    APP_NAME = "ARRMIS"

    INSTITUTION_NAME = "Academic Records & Resource Management Information System"

    ITEMS_PER_PAGE = 20

    # ==========================================
    # SECURITY
    # ==========================================
    REMEMBER_COOKIE_DURATION = 86400

    WTF_CSRF_ENABLED = True

    # ==========================================
    # EMAIL (Configure later)
    # ==========================================
    MAIL_SERVER = ""

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USERNAME = ""

    MAIL_PASSWORD = ""

    MAIL_DEFAULT_SENDER = ""