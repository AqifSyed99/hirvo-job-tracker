import os
from pathlib import Path
from dotenv import load_dotenv

# Always load .env from the backend/ directory regardless of where the script is run from
load_dotenv(dotenv_path=Path(__file__).parent / ".env")


class Config:
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    JWT_SECRET = os.environ.get("JWT_SECRET", "change-me-in-production")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Neon serverless closes idle connections — recycle and pre-ping to handle this
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,       # test connection before using it
        "pool_recycle": 300,         # recycle connections every 5 minutes
        "pool_size": 5,
        "max_overflow": 2,
        "connect_args": {"sslmode": "require"},
    }

    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "")

    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET = "test-secret"
