# from flask import Flask
# from app.models import db, migrate
#
# def create_app():
#     app = Flask(__name__)
#
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SECRET_KEY'] = 'qwerty_secret_key'
#     app.config['DEBUG'] = True
#
#     db.init_app(app)
#     migrate.init_app(app, db)
#
#     # Импорт моделей, чтобы SQLAlchemy их зарегистрировал
#     from app.models.category import Category
#     from app.models.questions import Question, Response, Statistic
#
#     # Здесь можно подключить Blueprints, если есть
#     # from app.routers.questions import questions_bp
#     # app.register_blueprint(questions_bp)
#
#     return app
#
#
from flask import Flask
from app.models import db, migrate  # импортируем db и migrate

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

    # Импорт моделей, чтобы SQLAlchemy их зарегистрировал
    # Импортировать **после инициализации db**
    from app.models.category import Category
    from app.models.questions import Question, Response, Statistic

    # Регистрация blueprints (если есть)
    # from app.routers.questions import questions_bp
    # app.register_blueprint(questions_bp)

    return app

