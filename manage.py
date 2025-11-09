# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routers.questions import questions_bp
from app.routers.response import response_bp
from config import DevelopmentConfig

# создаём объект миграций один раз
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # регистрация blueprints
    app.register_blueprint(questions_bp)
    app.register_blueprint(response_bp)

    return app
