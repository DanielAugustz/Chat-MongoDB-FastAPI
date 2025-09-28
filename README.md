FastAPI Chat (mínimo) + MongoDB Atlas

Passos
-Crie um cluster gratuito no MongoDB Atlas (https://cloud.mongodb.com).

-Em Database Access, crie um usuário e senha.

-Em Network Access, libere seu IP (ou 0.0.0.0/0 para testes).

-Copie a Connection String (driver MongoDB, mongodb+srv://...).

-Faça uma cópia de .env.example para .env e cole sua string na MONGO_URL.

-Rode localmente:


python -m venv .venv

Windows: .venv\Scripts\activate

Linux/Mac:

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


Abra: http://localhost:8000  (cliente simples)

Docs: http://localhost:8000/docs

Endpoints principais

-WebSocket**: ws://localhost:8000/ws/{room}

-Histórico REST**: GET /rooms/{room}/messages?limit=20

-Enviar (REST)**: POST /rooms/{room}/messages

