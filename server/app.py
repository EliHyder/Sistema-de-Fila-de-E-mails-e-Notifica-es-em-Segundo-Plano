from fastapi import FastAPI

from server.routers import emails

app = FastAPI()

app.include_router(emails.router)

@app.get("/")
async def read_root():
    return {"Sistema de Fila de E-mails e Notificações": "Bem-vindo ao sistema de fila de e-mails e notificações!"}