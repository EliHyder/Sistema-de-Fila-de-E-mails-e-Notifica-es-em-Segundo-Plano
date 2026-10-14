# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from datetime import datetime

# URL de conexão (exemplo usando SQLite localmente)
DATABASE_URL = "sqlite:///Fila.db"

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Cria a fábrica de sessões (SessionLocal) para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para criar os modelos de tabelas
Base = declarative_base()

from .models import User, Logs

Base.metadata.create_all(bind=engine)  # Cria as tabelas no banco de dados


# Função utilitária opcional para obter a sessão (muito usada em APIs)
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def create_user(db, name: str, email: str):
    try:
        new_user = User(
            name=name, 
            email=email, 
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()  # Desfaz a alteração se der erro (ex: e-mail duplicado)
        raise ValueError("Este e-mail já está cadastrado no sistema.")
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Erro ao salvar no banco de dados: {e}")

def find_user_by_email(db, email: str):
    try:
        return db.query(User).filter(User.email == email).first()
    except SQLAlchemyError as e:
        raise RuntimeError(f"Erro ao buscar usuário pelo e-mail: {e}")

def find_user_by_id(db, user_id: int):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError as e:
        raise RuntimeError(f"Erro ao buscar usuário pelo ID: {e}")

def create_log(db, user_id: int, subject: str, body: str): 
    try:
        log = db.query(Logs).filter(Logs.user_id == user_id, Logs.subject == subject, Logs.body == body).first()
        if log:
            log.attempts += 1  # Incrementa o número de tentativas
            db.commit()
            db.refresh(log)
            return log  # Retorna o log existente se já houver um com os mesmos detalhes
        new_log = Logs(
            user_id=user_id,
            subject=subject,
            body=body,
            status="pending",
            attempts=0,
            error_message=None,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=None
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log  
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Erro ao criar log de e-mail: {e}")

def update_log_status(db, log_id: int, status: str, error_message: str = None):
    try:
        log = db.query(Logs).filter(Logs.id == log_id).first()
        if log:
            log.status = status
        log.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if error_message:
            log.error_message = error_message
        db.commit()
        db.refresh(log)
        return log
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Erro ao atualizar status do log: {e}")
    

def get_next_pending_log(db):
    try:
      return db.query(Logs).filter(Logs.status == "pending").order_by(Logs.created_at.asc()).first()
    except SQLAlchemyError as e:
      raise RuntimeError(f"Erro ao buscar próximo log pendente: {e}")

def get_email_status(db, log_id: int):
    try:
        return db.query(Logs.id, Logs.status, Logs.attempts, Logs.error_message).filter(Logs.id == log_id).first()
    except SQLAlchemyError as e:
        raise RuntimeError(f"Erro ao buscar status do e-mail: {e}")

def get_log_by_id(db, log_id: int):
    try:
        return db.query(Logs).filter(Logs.id == log_id).first()
    except SQLAlchemyError as e:
        raise RuntimeError(f"Erro ao buscar log pelo ID: {e}")