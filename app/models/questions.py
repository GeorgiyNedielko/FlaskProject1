from . import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    responses = db.relationship('Response', backref='question', lazy=True)

    def __repr__(self):
        return f"<Question {self.id}: {self.text}>"

class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_agree = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Response {self.id} for Question {self.question_id}: {'agree' if self.is_agree else 'disagree'}>"

class Statistic(db.Model):
    __tablename__ = 'statistics'

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, default=0, nullable=False)
    disagree_count = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<Statistic for Question {self.question_id}: {self.agree_count} agree, {self.disagree_count} disagree>"
