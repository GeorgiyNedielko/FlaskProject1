from flask import jsonify
from app.models import db
from app import create_app
from app.models.category import Category
from app.models.questions import Question, Response

app = create_app()

def create_test_data():
    with app.app_context():
        db.create_all()

        if not Question.query.first():
            python_category = Category(name="Python")
            flask_category = Category(name="Flask")
            db.session.add_all([python_category, flask_category])
            db.session.commit()

            q1 = Question(text="Любите ли вы Python?", category=python_category)
            q2 = Question(text="Используете ли вы Flask?", category=flask_category)
            db.session.add_all([q1, q2])
            db.session.commit()
            print("Добавлены тестовые данные!")

create_test_data()

@app.route('/')
def home():
    return "Добро пожаловать в Community Pulse! Перейдите к /questions/ чтобы увидеть вопросы."

@app.route('/questions/', methods=['GET'])
def list_questions():
    questions = Question.query.all()
    data = [
        {
            'id': q.id,
            'text': q.text,
            'category': q.category.name if getattr(q, 'category', None) else None
        }
        for q in questions
    ]
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(debug=True)
