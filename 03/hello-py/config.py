import os


class Config:
    DEBUG = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    GREETING = os.getenv("GREETING", "Hello")
    HOSTNAME = os.environ['HOSTNAME']
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql:///crud").rstrip()

    # Work around for heroku
    # https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
