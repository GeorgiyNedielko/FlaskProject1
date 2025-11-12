#app/schemas/question.py
from pydantic import BaseModel, Field

class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=12)

class QuestionResponse(BaseModel):
    id: int
    text: str

class MessageResponse(BaseModel):
    message: str
