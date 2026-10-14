from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse, EmailRequest, EmailResponse, EmailStatusResponse
from DB.db import get_db, create_user as db_create_user, create_log, get_email_status
from worker import enqueue_email_task

router = APIRouter(
    prefix="/emails",
    tags=["emails"]
)

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Passando os campos corretos que o db.py espera
        created_user = db_create_user(db, name=user.name, email=user.email)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send", response_model=EmailResponse, status_code=status.HTTP_201_CREATED)
async def send_email(email: EmailRequest, db: Session = Depends(get_db)):
    try:
        created_email = create_log(db, user_id=email.user_id, subject=email.subject, body=email.body)
        
        # ⚠️ É AQUI QUE ENTRARÁ O RQ (REDIS) PARA ENFILEIRAR A TAREFA EM SEGUNDO PLANO!
        enqueue_email_task(log_id=created_email.id)

        return created_email
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{id}", response_model=EmailStatusResponse)
async def check_email_status(id: int, db: Session = Depends(get_db)):
    try:
        email_status = get_email_status(db, id)
        if email_status is None:
            raise HTTPException(status_code=404, detail="Email not found")
        return email_status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))