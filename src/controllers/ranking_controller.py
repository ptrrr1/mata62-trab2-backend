import logging
from sqlalchemy import select, func, desc, case

from model import dbmanager
from model.models import Session, UserAnswer, User, Question

logger = logging.getLogger(__name__)

class RankingController:

    @staticmethod
    def get_quiz_ranking(quiz_id: int):
        s = dbmanager.session

        logger.info(f"Gerando ranking para Quiz ID: {quiz_id}")

        stmt = (
            select(
                User.username,
                Session.start_time,
                Session.end_time,

                func.sum(
                    case(
                        (UserAnswer.is_correct == True, 1),
                        else_=0
                    )
                ).label("score")
            )
            .select_from(Session)
            .join(User, Session.user_id == User.id)
            .outerjoin(UserAnswer, Session.id == UserAnswer.session_id)
            .where(
                Session.quiz_id == quiz_id,
                Session.end_time.isnot(None)
            )
            .group_by(Session.id, User.username, Session.start_time, Session.end_time)
        )

        result = s.execute(stmt).all()
        
        ranking_data = []

        for row in result:
            username, start, end, score = row
            
            # Garante que score seja um número (pode vir None ou Decimal do banco)
            final_score = int(score) if score else 0

            duration = 0.0
            if start and end:
                duration = (end - start).total_seconds()

            ranking_data.append({
                "username": username,
                "score": final_score,
                "duration": duration,
                "end_time": end
            })

        ranking_data.sort(key=lambda x: (-x['score'], x['duration']))

        return ranking_data

    @staticmethod
    def get_global_ranking():
        s = dbmanager.session
        stmt = (
            select(
                User.username,
                func.count(UserAnswer.id).label("total_score"),
                func.count(func.distinct(Session.quiz_id)).label("quizzes_played")
            )
            .join(User, Session.user_id == User.id)
            .join(UserAnswer, (Session.id == UserAnswer.session_id) & (UserAnswer.is_correct == True))
            .group_by(User.id, User.username)
            .order_by(desc("total_score"))
        )

        return s.execute(stmt).all()
    
    @staticmethod
    def get_questions_dashboard(quiz_id: int = None):
        s = dbmanager.session
        try:
            stmt = (
                select(
                    Question.id,
                    Question.text,
                    func.count(UserAnswer.id).label("total_attempts"),
                    func.sum(case((UserAnswer.is_correct == True, 1), else_=0)).label("correct_count")
                )
                .join(UserAnswer, Question.id == UserAnswer.question_id)
                .group_by(Question.id, Question.text)
                .order_by(desc("total_attempts")) 
            )
            
            if quiz_id:
                stmt = stmt.where(Question.quiz_id == quiz_id)

            results = s.execute(stmt).all()
            
            dashboard_data = []
            for row in results:
                q_id, text, total, correct = row
                correct = correct or 0 # Tratar None
                accuracy = (correct / total * 100) if total > 0 else 0.0
                
                dashboard_data.append({
                    "question_id": q_id,
                    "text": text,
                    "total_attempts": total,
                    "correct_count": int(correct),
                    "wrong_count": total - int(correct),
                    "accuracy_percent": round(accuracy, 2)
                })
                
            return dashboard_data

        except Exception as e:
            logger.error(f"Erro no dashboard de questões: {e}")
            return []
