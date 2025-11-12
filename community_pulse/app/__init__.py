from flask import Flask
from .models import db, migrate

def create_app():
    app = Flask(__name__)

    # Конфиг приложения
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'qwerty_secret_key'
    app.config['DEBUG'] = True

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # Импорт моделей
    from .models.category import Category
    from .models.questions import Question, Response, Statistic

    # Регистрируем blueprint (ОБЯЗАТЕЛЬНО внутри create_app)
    from app.routers.questions import questions_bp
    app.register_blueprint(questions_bp)

    from app.routers.response import response_bp
    app.register_blueprint(response_bp)

    return app
