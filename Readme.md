# AI Question Generator — Agentic App

An AI-powered exam practice question generator built with FastAPI, LangChain, and a swappable multi-LLM adapter system.

![App Screenshot](https://github.com/user-attachments/assets/94f5196b-bfc0-4429-9412-8ce8812ec317)

---

## Features

- Generate practice questions for JEE, NEET, SAT, GATE, UPSC
- Supports subjects: Mathematics, Physics, Chemistry, Biology, Computer Science
- Chat history support — context-aware multi-turn generation
- Swappable LLM providers: LangChain, Gemini, Cohere — change one line in `.env`
- Clean REST API with FastAPI + interactive frontend

---

## Project Structure

```
AgenticApp/
├── agents/                  # (multi-agent folder — add agents here)
├── static/
│   ├── index.html           # Frontend UI
│   ├── app.js               # Frontend logic
│   └── style.css
├── agent.py                 # Core question generation logic
├── context_store.py         # Subject/exam context metadata
├── llm_adapter.py           # LLM adapter (LangChain | Gemini | Cohere)
├── main.py                  # FastAPI app entry point
├── models.py                # Pydantic request/response models
├── .env                     # API keys and config (never commit)
├── .env.example             # Template for .env
└── requirements.txt
```

---

## Setup

**1. Clone and install dependencies**

```bash
git clone https://github.com/sarveshhome/QuestionAgenticApp.git
cd AgenticApp
pip3 install -r requirements.txt
```

**2. Configure environment**

```bash
cp .env.example .env
```

Edit `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
COHERE_API_KEY=your_cohere_api_key
COHERE_MODEL=command-r7b-12-2024

# Switch provider: langchain | gemini | cohere
LLM_PROVIDER=langchain
```

**3. Run the application**

```bash
python3 -m uvicorn main:app --reload
```

Open → http://localhost:8000

---

## Switching LLM Providers

Change a single line in `.env` — no code changes needed:

| Provider | `LLM_PROVIDER` value | Key Required |
|---|---|---|
| LangChain + Gemini | `langchain` | `GEMINI_API_KEY` |
| Gemini (direct) | `gemini` | `GEMINI_API_KEY` |
| Cohere | `cohere` | `COHERE_API_KEY` |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Frontend UI |
| `POST` | `/api/generate` | Generate questions |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/subjects` | List subjects & exam types |

**POST `/api/generate` — Request body:**

```json
{
  "subject": "Mathematics",
  "exam_type": "JEE",
  "num_questions": 2,
  "chat_history": []
}
```

---

## Adding a New LLM Adapter

1. Add a new class in `llm_adapter.py` extending `LLMAdapter`:

```python
class MyAdapter(LLMAdapter):
    def generate(self, system_prompt, user_prompt, chat_history=None) -> str:
        # your implementation
        ...
```

2. Register it in `get_adapter()`:

```python
adapters = {
    "langchain": LangChainAdapter,
    "gemini": GeminiAdapter,
    "cohere": CohereAdapter,
    "myprovider": MyAdapter,   # add here
}
```

3. Set in `.env`:

```env
LLM_PROVIDER=myprovider
```

---

## Supported Exams & Subjects

| Subject | JEE | NEET | SAT | GATE | UPSC |
|---|---|---|---|---|---|
| Mathematics | ✅ | | ✅ | ✅ | |
| Physics | ✅ | ✅ | | ✅ | |
| Chemistry | ✅ | ✅ | | | |
| Biology | | ✅ | | | ✅ |
| Computer Science | | | ✅ | ✅ | |

---

## Get API Keys

- Gemini → https://aistudio.google.com/app/apikey
- LangChain → https://smith.langchain.com/settings
- Cohere → https://dashboard.cohere.com/api-keys


agents/
├── __init__.py         ← exports QuestionAgent, ReviewAgent
├── base_agent.py       ← shared base (holds LLM adapter)
├── question_agent.py   ← reads metadata/ → generates questions
└── review_agent.py     ← reads metadata/ → reviews questions



create multi-agent system 
multi-agent will read from folder 
store all qustion in one metadata folder


### Run the application

`python3 -m uvicorn main:app --reload`

<img width="3008" height="1720" alt="image" src="https://github.com/user-attachments/assets/94f5196b-bfc0-4429-9412-8ce8812ec317" />




