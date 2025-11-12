# app/routers/response.py
from flask import Blueprint, request, jsonify
from app.models import db
from app.models.questions import Question, Response, Statistic  # импортируем нужные модели

response_bp = Blueprint('responses', __name__, url_prefix='/responses')

@response_bp.route('/', methods=['GET'])
def get_responses():
    """Получение статистики ответов."""
    stats = Statistic.query.all()
    result = [
        {
            "question_id": s.question_id,
            "agree_count": s.agree_count,
            "disagree_count": s.disagree_count
        }
        for s in stats
    ]
    return jsonify(result), 200

@response_bp.route('/', methods=['POST'])
def add_response():
    """Добавление нового ответа на вопрос с обновлением статистики."""
    data = request.get_json()

    if not data or 'question_id' not in data or 'is_agree' not in data:
        return jsonify({'message': "Некорректные данные"}), 400

    question = Question.query.get(data['question_id'])
    if not question:
        return jsonify({'message': "Вопрос не найден"}), 404

    # Создаём ответ
    response = Response(question_id=question.id, is_agree=bool(data['is_agree']))
    db.session.add(response)

    # Обновляем/создаём статистику
    stat = Statistic.query.filter_by(question_id=question.id).first()
    if not stat:
        stat = Statistic(question_id=question.id, agree_count=0, disagree_count=0)
        db.session.add(stat)

    if response.is_agree:
        stat.agree_count += 1
    else:
        stat.disagree_count += 1

    db.session.commit()
    return jsonify({'message': f"Ответ на вопрос {question.id} добавлен"}), 201
