# app/models/response.py
from app import db


class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_agree = db.Column(db.Boolean, nullable=False)  # True — согласен, False — не согласен

    def __repr__(self):
        return f'<Response {self.id} for Question {self.question_id}: {"agree" if self.is_agree else "disagree"}>'
