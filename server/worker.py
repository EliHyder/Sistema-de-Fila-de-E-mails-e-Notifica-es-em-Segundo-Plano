from redis import Redis
from rq import Worker, Queue, Connection
from tasks import send_email_task

# Conexão com o Redis
conn = Redis(host='localhost', port=6379, db=0)
fila = Queue(connection=conn)

def enqueue_email_task(log_id: int):
    """Enfileira a tarefa de envio de e-mail no RQ."""
    job = fila.enqueue(send_email_task, log_id=log_id)
    return job

# Bloco para rodar o worker diretamente pelo terminal com 'python worker.py'
if __name__ == '__main__':
    with Connection(conn):
        worker = Worker([fila])
        worker.work()