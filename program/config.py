import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATION = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        URI_VARS = [
            "DB_USER", 
            "DB_PASS", 
            "DB_NAME", 
            "DB_DOMAIN"
        ]
        uri_dict = {item: os.environ.get(item) for item in URI_VARS}
        if not all(uri_dict.values()):
            raise ValueError("Database configuration error. At least one key is missing.")
        return f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_DOMAIN}/{DB_NAME}"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()