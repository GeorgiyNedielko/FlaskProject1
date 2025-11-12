# app/routers/questions.py
from flask import Blueprint, jsonify, request
from dataclasses import dataclass
from typing import Optional

from app.models import db
from app.models.questions import Question
from app.schemas.question import QuestionCreate, QuestionResponse
from pydantic import ValidationError

# 1) СНАЧАЛА объявляем blueprint
questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

# 2) Контракты
@dataclass
class QuestionData:
    text: str

@dataclass
class ErrorResponse:
    error: str

@dataclass
class SuccessResponse:
    message: str
    id: Optional[int] = None

# 3) Роуты
# @questions_bp.route('/', methods=['GET'])
# def get_questions():
#     questions = Question.query.all()
#     questions_data = [{'id': q.id, 'text': q.text} for q in questions]
#     return jsonify(questions_data), 200

# @questions_bp.route('/', methods=['POST'])
# def create_question():
#     """Создание нового вопроса с контрактом."""
#     try:
#         payload = request.get_json(force=True, silent=False)
#         data = QuestionData(**payload)
#     except Exception:
#         return jsonify(ErrorResponse("Некорректные данные запроса").__dict__), 400
#
#     if not data.text.strip():
#         return jsonify(ErrorResponse("Текст вопроса не может быть пустым").__dict__), 400
#
#     question = Question(text=data.text)
#     db.session.add(question)
#     db.session.commit()
#
#     return jsonify(SuccessResponse("Вопрос создан", id=question.id).__dict__), 201


@questions_bp.route('/', methods=['POST'])
def create_question():
    """Создание нового вопроса с контрактом (Pydantic)."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Expected JSON body"}), 400

    try:
        question_data = QuestionCreate(**data)   # валидация входа
    except ValidationError as e:
        return jsonify(e.errors()), 400          # детальные ошибки схемы

    # бизнес-логика
    question = Question(text=question_data.text.strip())
    db.session.add(question)
    db.session.commit()

    # формируем ответ контрактом
    resp = QuestionResponse(id=question.id, text=question.text)
    return jsonify(resp.dict()), 201

# @questions_bp.route('/<int:id>', methods=['GET'])
# def get_question(id):
#     question = Question.query.get(id)
#     if question is None:
#         return jsonify({'message': "Вопрос с таким ID не найден"}), 404
#     return jsonify({'message': f"Вопрос: {question.text}"}), 200
@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Список вопросов (возвращаем через схемы ответа)."""
    items = Question.query.all()
    payload = [QuestionResponse(id=q.id, text=q.text).dict() for q in items]
    return jsonify(payload), 200

@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    question = Question.query.get(id)
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404
    data = request.get_json() or {}
    if 'text' not in data or not str(data['text']).strip():
        return jsonify({'message': "Текст вопроса не предоставлен"}), 400
    question.text = data['text']
    db.session.commit()
    return jsonify({'message': f"Вопрос обновлен: {question.text}"}), 200

@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f"Вопрос с ID {id} удален"}), 200

