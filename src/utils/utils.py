from src.controllers.answer_controller import AnswerController

answer_controller=AnswerController()
def calculate_score(answers, correct_answers):
    score = 0
    for question_id, answer in answers.items():
        if question_id in correct_answers and answer == correct_answers[question_id]:
            score += 1
    return score

def check_answer(question_id, user_answer):
    answer=answer_controller.get_correct_answer_by_question(question_id)
    
    if answer.id == user_answer:
        return True
    else:
        return False
  