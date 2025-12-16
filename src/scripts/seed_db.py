import sys
import os

# Adiciona o diretório raiz ao path para conseguir importar 'src'
sys.path.append(os.getcwd())

from src.model import dbmanager
from src.model.models import User, Team, Quiz, Question, Answer
from sqlalchemy import text

def seed():
    session = dbmanager.session
    print("🌱 Iniciando o Seeding do Banco de Dados...")

    try:
        #**** Remove this comments if you want to delete old data ****
        # 1. Limpar dados antigos (Opcional - CUIDADO EM PRODUÇÃO)
        # print("🧹 Limpando dados antigos...")
        # session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        # session.execute(text("TRUNCATE TABLE user_answers;"))
        # session.execute(text("TRUNCATE TABLE sessions;"))
        # session.execute(text("TRUNCATE TABLE answers;"))
        # session.execute(text("TRUNCATE TABLE questions;"))
        # session.execute(text("TRUNCATE TABLE quizzes;"))
        # session.execute(text("TRUNCATE TABLE teams;"))
        # session.execute(text("TRUNCATE TABLE users;"))
        # session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        # session.commit()
        if session.query(User).first():
            print("⚠️ Banco já populado. Seed ignorado.")
            session.close()
            return
        # 2. Criar Usuários
        print("👤 Criando Usuários...")
        admin = User(
            username="admin", 
            email="admin@futquiz.com", 
            hashed_password=User.hash_password("admin123"), 
            role="admin"
        )
        player1 = User(
            username="ney_mar", 
            email="ney@brasil.com", 
            hashed_password=User.hash_password("123456"), 
            role="user"
        )
        player2 = User(
            username="messi_10", 
            email="leo@argentina.com", 
            hashed_password=User.hash_password("123456"), 
            role="user"
        )
        
        session.add_all([admin, player1, player2])
        session.commit() # Comita para gerar os IDs

        # 3. Criar Times
        print("⚽ Criando Times...")
        fla = Team(name="Flamengo")
        real = Team(name="Real Madrid")
        city = Team(name="Manchester City")
        
        session.add_all([fla, real, city])
        session.commit()

        # 4. Criar Quizzes
        print("📝 Criando Quizzes...")
        quiz_fla = Quiz(team_id=fla.id, is_active=True)
        quiz_real = Quiz(team_id=real.id, is_active=True)
        
        session.add_all([quiz_fla, quiz_real])
        session.commit()

        # 5. Criar Perguntas e Respostas (Flamengo)
        print("❓ Criando Perguntas (Flamengo)...")
        
        # Pergunta 1
        q1 = Question(quiz_id=quiz_fla.id, text="Em que ano o Flamengo ganhou a primeira Libertadores?", is_active=True)
        session.add(q1)
        session.commit()
        
        session.add_all([
            Answer(question_id=q1.id, text="1981", is_correct=True),
            Answer(question_id=q1.id, text="2019", is_correct=False),
            Answer(question_id=q1.id, text="1990", is_correct=False),
            Answer(question_id=q1.id, text="1954", is_correct=False),
        ])

        # Pergunta 2
        q2 = Question(quiz_id=quiz_fla.id, text="Quem é o maior ídolo da história do clube?", is_active=True)
        session.add(q2)
        session.commit()

        session.add_all([
            Answer(question_id=q2.id, text="Gabigol", is_correct=False),
            Answer(question_id=q2.id, text="Zico", is_correct=True),
            Answer(question_id=q2.id, text="Junior", is_correct=False),
        ])

        # 6. Criar Perguntas e Respostas (Real Madrid)
        print("❓ Criando Perguntas (Real Madrid)...")
        
        # Pergunta 3
        q3 = Question(quiz_id=quiz_real.id, text="Quantas Champions League o Real Madrid tinha até 2024?", is_active=True)
        session.add(q3)
        session.commit()

        session.add_all([
            Answer(question_id=q3.id, text="15", is_correct=True),
            Answer(question_id=q3.id, text="10", is_correct=False),
            Answer(question_id=q3.id, text="13", is_correct=False),
        ])

        session.commit()
        print("✅ Seeding concluído com SUCESSO!")

    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao popular banco: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed()