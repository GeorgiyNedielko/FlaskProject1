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

@app.route('/questions/')
def list_questions():
    questions = Question.query.all()
    return "<br>".join([f"{q.id}: {q.text} (Категория: {q.category.name})" for q in questions])

if __name__ == "__main__":
    app.run(debug=True)
