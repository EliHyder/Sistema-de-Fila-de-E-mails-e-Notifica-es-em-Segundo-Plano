# Sistema de Fila de E-mails e Notificações em Segundo Plano (Background Jobs)

Um sistema robusto de back-end desenvolvido em Python para gerenciar o envio assíncrono de e-mails e notificações, evitando gargalos na API principal através de filas de mensagens.

---

## 🚀 Sobre o Projeto

Em aplicações web de alta escala, operações demoradas ou propensas a falhas de rede (como o disparo de e-mails, processamento de relatórios ou integração com APIs externas) não devem bloquear a resposta ao usuário. 

Este projeto implementa uma arquitetura orientada a filas:
1. **A API** recebe a requisição de envio, registra o status inicial como `pendente` no banco de dados e enfileira a tarefa instantaneamente.
2. **O Cliente** recebe uma resposta imediata de sucesso ("Na fila").
3. **O Worker** processa a tarefa de forma assíncrona em segundo plano, simulando o envio e atualizando o status final no banco.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI:** Framework web moderno e de alto desempenho para construção da API.
* **SQLAlchemy & Alembic:** ORM e gerenciamento de migrações para o banco de dados relacional.
* **PostgreSQL:** Banco de dados relacional para persistência de usuários e logs de envio.
* **Redis:** Servidor de estrutura de dados em memória, utilizado como *broker* de mensagens.
* **RQ (Redis Queue):** Biblioteca leve para enfileiramento de tarefas em Python.
* **Pydantic:** Validação robusta de dados baseada em tipagem.

---

## 📁 Estrutura do Diretório

```text
📁 Sistema de Fila de E-mails...
│
├── 📁 server/
│   ├── 📁 DB/
│   │   ├── db.py          # Conexão e gerenciamento de sessão do banco
│   │   └── models.py      # Definição das tabelas (Users, EmailLogs)
│   │
│   ├── 📁 routers/
│   │   └── emails.py      # Endpoints da API para enfileirar e consultar status
│   │
│   ├── app.py             # Inicialização da aplicação FastAPI
│   ├── config.py          # Configurações de ambiente
│   ├── schemas.py         # Contratos de entrada e saída (Pydantic)
│   ├── tasks.py           # Lógica de negócio da tarefa (envio de e-mail)
│   └── worker.py          # Script executor do worker da fila
│
├── 📁 client/             # Scripts opcionais de teste ou simulação de carga
├── 📁 venv/               # Ambiente virtual do Python
└── requirements.txt       # Dependências do projeto