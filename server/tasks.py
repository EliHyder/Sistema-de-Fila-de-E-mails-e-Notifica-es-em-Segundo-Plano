from DB.db import get_db, get_log_by_id, update_log_status
from time import sleep

def send_email_task(log_id: int):
    db = next(get_db())
    log = get_log_by_id(db, log_id)
    if not log:
        raise ValueError(f"Log with ID {log_id} not found.")
    
    # Aqui você implementaria a lógica real de envio de e-mail.
    # Por exemplo, usando uma biblioteca como smtplib ou um serviço de terceiros.
    try:
        # Simulação de envio de e-mail
        print(f"Enviando e-mail para {log.user_id} com assunto '{log.subject}'")

        sleep(2)  # Simula o tempo de envio do e-mail
        
        # Se o envio for bem-sucedido, atualize o status do log
        update_log_status(db, log_id=log.id, status="sent")
    except Exception as e:
        # Se houver um erro no envio, atualize o status do log para "failed"
        update_log_status(db, log_id=log.id, status="failed", error_message=str(e))