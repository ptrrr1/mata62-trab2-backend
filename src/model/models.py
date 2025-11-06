from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TeamController(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    quizzes = relationship("Quiz", back_populates="team")
    questions = relationship("Question", back_populates="team")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    team = relationship("Team", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    text = Column(Text, nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
    team = relationship("Team", back_populates="questions")
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)

    question = relationship("Question", back_populates="answers")
