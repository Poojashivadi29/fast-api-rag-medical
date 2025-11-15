# Fast API RAG Medical Appointment Scheduling Agent

A FastAPI-based medical appointment scheduling system with RAG (Retrieval-Augmented Generation) for answering clinic FAQs, Calendly integration, and AI-powered booking agent.

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Poojashivadi29/fast-api-rag-medical.git
cd fast-api-rag-medical
```

### 2. Set Up Environment Variables
Copy `.env.example` to `.env` and add your API keys:
```bash
cp .env.example .env
```

Then edit `.env` file and fill in your secrets:
```dotenv
OPENAI_API_KEY=sk-your-key-here
CALENDLY_API_TOKEN=your-token-here
```

**⚠️ Important:** Never commit `.env` to Git. It's in `.gitignore` by default.

### 3. Install Dependencies
```bash
# Full installation (includes RAG dependencies)
pip install -r requirements.txt

# OR minimal installation (for Windows without faiss)
pip install fastapi uvicorn[standard] python-dotenv sqlmodel alembic pydantic python-dateutil pytz requests nltk numpy
```

### 4. Run the Server
```bash
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open your browser:
- **Interactive API Docs:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

---

## 📋 How to Add Your API Keys

### OpenAI API Key (for Embeddings & LLM)
1. Go to https://platform.openai.com/api-keys
2. Click **Create new secret key**
3. Copy the key and add to `.env`:
   ```dotenv
   OPENAI_API_KEY=sk-...
   ```

### Calendly API Token (for Calendar Integration)
1. Go to https://calendly.com/settings/integrations/api_tokens
2. Click **Generate a new token**
3. Copy the token and add to `.env`:
   ```dotenv
   CALENDLY_API_TOKEN=...
   ```

---

## 🐳 Using Docker

```bash
docker compose up --build
```

The app will be available at http://localhost:8000

---

## 📁 Project Structure

```
fast-api-rag-medical/
├── backend/
│   ├── api/              # FastAPI routes (calendly, chat)
│   ├── agent/            # Scheduling agent logic
│   ├── rag/              # RAG (embeddings, vector store)
│   ├── tools/            # Availability and booking tools
│   ├── db.py             # Database models
│   ├── main.py           # FastAPI app entry point
│   └── models.py         # Pydantic models
├── data/                 # Clinic FAQ data
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── Dockerfile            # Docker configuration
└── docker-compose.yml    # Docker Compose configuration
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Redirect to API docs |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive Swagger UI |
| GET | `/api/calendly/availability` | Get provider availability |
| POST | `/api/calendly/book` | Create a booking |
| POST | `/api/agent/query` | Query the scheduling agent |

---

## ⚙️ Environment Variables

See `.env.example` for all available configuration options:

- `APP_TZ` - Application timezone (default: `Asia/Kolkata`)
- `DATABASE_URL` - SQLite database path
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `CALENDLY_API_TOKEN` - Calendly API token (optional)
- `LLM_PROVIDER` - Use `local` or `openai`
- `VECTOR_DB` - Use `faiss`

---

## 📝 Features

✅ Calendly integration for provider availability  
✅ RAG for medical FAQ retrieval  
✅ AI-powered scheduling agent  
✅ SQLite database for bookings  
✅ Interactive Swagger API docs  
✅ Docker support  

---

## 📝 License

MIT

