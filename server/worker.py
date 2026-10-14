from redis import Redis
from rq import SimpleWorker, Queue
from tasks import send_email_task

# Conexão com o Redis
conn = Redis(host='localhost', port=6379, db=0)

# Passa a conexão explicitamente para a fila
fila = Queue('default', connection=conn)

def enqueue_email_task(log_id: int):
    """Enfileira a tarefa de envio de e-mail no RQ."""
    job = fila.enqueue(send_email_task, log_id=log_id)
    return job

# Execute com `python -m server.worker` a partir da raiz do projeto.
if __name__ == '__main__':
    # Passa a conexão diretamente para o Worker
    worker = SimpleWorker([fila], connection=conn)
    worker.work()