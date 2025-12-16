from controllers.answer_controller import AnswerController

answer_controller=AnswerController()
def calculate_score(correct_answers):
    score=len(correct_answers)
    return score

def check_answer(question_id, user_answer):
    answer=answer_controller.get_correct_answer_by_question(question_id)
    
    if answer.id == user_answer:
        return True
    else:
        return False
  
