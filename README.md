# Sistema de Fila de E-mails e Notificações em Segundo Plano

Um sistema robusto de back-end desenvolvido em **Python** para gerenciamento de filas de tarefas assíncronas, garantindo que o processamento pesado (como o envio de e-mails) ocorra em segundo plano sem bloquear as requisições da API.

---

## 🛠️ Tecnologias Utilizadas

- **Python** (Linguagem principal)
- **FastAPI** (Framework web para a construção da API REST)
- **SQLAlchemy + SQLite / PostgreSQL** (ORM e banco de dados relacional)
- **Pydantic** (Validação de dados e contratos)
- **Redis & RQ (Redis Queue)** (Broker de mensagens e gerenciador de filas assíncronas)
- **Docker Desktop** (Para execução do servidor Redis localmente)

---

## 📂 Estrutura do Projeto

O projeto está organizado da seguinte forma dentro da pasta `server`:

```text
Sistema de Fila de E-mails e Notificações/
│
├── venv/                      # Ambiente virtual Python
├── README.md                  # Documentação do projeto
└── server/                    # Pasta principal da aplicação
    ├── app.py                 # Ponto de entrada do FastAPI
    ├── worker.py              # Script do Worker e enfileirador do RQ
    ├── tasks.py               # Lógica de execução da tarefa em segundo plano
    ├── DB/
    │   ├── db.py              # Configuração da sessão e funções do banco
    │   └── models.py          # Modelos das tabelas (User, Logs)
    ├── schemas.py             # Schemas Pydantic de entrada e saída
    └── routers/
        └── emails.py          # Endpoints da API (Usuários e E-mails)
```

---

## ⚙️ Pré-requisitos

Certifique-se de ter instalado na sua máquina:
1. **Python** (versão recente)
2. **Docker Desktop** (para rodar o Redis)

---

## 🚀 Como Executar o Projeto Passo a Passo

Siga os passos abaixo para colocar o sistema de ponta a ponta em funcionamento:

### 1. Iniciar o Servidor Redis (via Docker)
Abra qualquer terminal e execute o comando para subir o container do Redis na porta padrão `6379`:
```bash
docker run --name meu-redis -p 6379:6379 -d redis
```

### 2. Ativar o Ambiente Virtual
No terminal principal do seu projeto, ative o ambiente virtual (`venv`):
- **No Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- **No Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```

### 3. Entrar na Pasta `server`
Como a estrutura principal do projeto reside na pasta `server`, navegue até ela:
```bash
cd server
```

### 4. Executar o Worker (Terminal 1)
Em um primeiro terminal (já dentro da pasta `server` e com o `venv` ativo), execute o worker para começar a escutar a fila do Redis:
```bash
python worker.py
```
*Deixe este terminal aberto. Ele ficará aguardando e processando as tarefas em segundo plano.*

### 5. Executar a API FastAPI (Terminal 2)
Abra um **segundo terminal**, ative o ambiente virtual, entre na pasta `server` e inicie o Uvicorn com o *reloading* automático:
```bash
cd server
uvicorn app:app --reload
```

---

## 🧪 Como Testar a Aplicação

Com a API rodando, abra o seu navegador e acesse a documentação interativa automática do FastAPI:
👉 **`http://127.0.0.1:8000/docs`**

Através do Swagger UI, você pode:
1. **Cadastrar um Usuário:** Envie os dados na rota `POST /emails/users`.
2. **Enviar um E-mail:** Envie uma solicitação na rota `POST /emails/send`. O sistema criará o log como `pending` no banco, jogará a tarefa no Redis e responderá imediatamente.
3. **Acompanhar o Processamento:** Olhe para o terminal onde o `worker.py` está rodando e veja a simulação do envio após alguns segundos.
4. **Consultar o Status:** Use a rota `GET /emails/status/{id}` para verificar se o status mudou de `pending` para `sent`.