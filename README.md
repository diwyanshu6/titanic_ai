# 🚢 Titanic AI — Intelligent Hybrid Data Assistant (Production-Ready)

Titanic AI is a hybrid analytics system that intelligently answers questions about the Titanic dataset using a safe, production-ready routing architecture.

It combines:

- ⚡ Deterministic rule-based analytics (zero hallucination)
- 📊 Dynamic data visualizations
- 🧠 LLM-powered reasoning (Groq + LangChain)
- 🏗 Modular backend architecture
- 📦 Structured production logging
- 🚀 Cloud deployment (Render + Streamlit Cloud)

This project demonstrates how to safely integrate LLMs into real-world backend systems without sacrificing reliability, performance, cost efficiency, or performance speed.

---

# 🌍 Live Deployment

## Backend (FastAPI on Render)
Production API serving `/chat` endpoint.

## Frontend (Streamlit Cloud)
Interactive UI connected to deployed backend.

The system is fully production-accessible.

---

# 🧠 Problem This Project Solves

LLMs are powerful — but:

- They hallucinate
- They are expensive
- They are slower than deterministic logic
- They can hit rate limits

## ✅ Solution: 3-Layer Intelligent Routing Architecture

The system routes queries in this order:

Deterministic Engine → Visualization Engine → LLM Engine

LLM is used only when absolutely necessary.

This ensures:

- Maximum reliability
- Minimum hallucination risk
- Low API cost
- Fast response time
- Production safety

---

# 🏗 System Architecture

User (Streamlit UI)  
        │  
        ▼  
FastAPI Backend (/chat)  
        │  
        ▼  
TitanicAgentService (Router)  
        │  
 ┌───────────────┬───────────────┬───────────────┐  
 │               │               │  
 ▼               ▼               ▼  
Deterministic   Visualization    LLM Engine  
Engine          Engine           (Groq + LangChain)  

---

# 🔄 Routing Strategy

## 🟢 Layer 1 — Deterministic Engine (Priority 1)

Handles:

- Counts  
- Multi-filter queries  
- Percentages  
- Grouped counts  
- Survival rate  
- Mean / Max / Min  
- Gender filtering  
- Class filtering  
- Survival filtering  

Why deterministic first?

- No hallucination  
- Instant response  
- Zero API usage  
- Fully production-safe  

If matched → returns immediately.  
LLM is never called.

---

## 🔵 Layer 2 — Visualization Engine

Triggered only when query contains:

plot, chart, histogram, scatter, line, boxplot, pie, bar

Generates:

- Matplotlib chart  
- Base64-encoded image  
- Clean structured JSON response  

No LLM involved. Fully deterministic.

---

## 🟣 Layer 3 — LLM Engine (Groq + LangChain)

Used only when:

- Deterministic logic cannot answer  
- Query requires reasoning  
- Correlation or interpretation needed  

Features:

- Pandas DataFrame Agent  
- max_iterations limit (prevents infinite loops)  
- Timeout handling  
- Rate-limit (429) handling  
- Exception protection  
- Structured logging  

---

# 📁 Project Structure
titanic_ai/
│
├── backend/
│ ├── main.py
│ │
│ ├── core/
│ │ ├── config.py
│ │ ├── exceptions.py
│ │ ├── exceptions_handler.py
│ │ └── logging_config.py
│ │
│ ├── services/
│ │ ├── agent_service.py
│ │ ├── deterministic_engine.py
│ │ ├── visualization_engine.py
│ │ └── llm_engine.py
│ │
│ ├── schemas/
│ │ └── chat.py
│ │
│ └── data/
│ └── titanic.csv
│
├── frontend/
│ └── app.py
│
├── requirements.txt
└── README.md


---

# 🧩 Core Components Explained

## 1️⃣ DeterministicEngine

Rule-based analytics engine.

Supports:

- Gender filtering  
- Class filtering  
- Survival filtering  
- Multi-filter queries  
- Grouped counts  
- Percentages  
- Survival rate analysis  
- Numeric operations (mean, max, min)  

Key Design Decisions:

- Grouped logic evaluated before total count  
- Prevents wrong early returns  
- Avoids unnecessary LLM calls  
- Ensures deterministic reliability  

---

## 2️⃣ VisualizationEngine

Handles explicit visual requests.

Supported plots:

- Histogram  
- Scatter plot  
- Line plot  
- Boxplot  
- Pie chart  
- Bar chart  

Returns:

- Base64 encoded image  
- Structured JSON response  

Fully deterministic, no hallucination risk.

---

## 3️⃣ LLMEngine

Powered by:

- Groq API  
- LangChain Pandas Agent  

Safety Mechanisms:

- max_iterations limit  
- Rate limit handling (429)  
- Timeout handling  
- Parsing error protection  
- Fallback safety  

Used only when deterministic fails.

---

# 📊 Logging System

Structured JSON logging implemented using a custom formatter.

Logs include:

- request_id  
- query  
- latency  
- visualization flag  
- token usage  
- hallucination detection flag  

Example:

Rotating file handler included.

---

# 🔐 Safety & Reliability Features

- Deterministic-first routing  
- LLM iteration limit  
- Timeout protection  
- Rate-limit retry handling  
- Structured exception handling  
- Invalid query detection  
- JSON response standardization  

---

# 🚀 Deployment

## Backend (Render)

Start Command:
uvicorn backend.main:app --host 0.0.0.0 --port 10000

Environment Variables:

- GROQ_API_KEY  
- MODEL_NAME  

---

## Frontend (Streamlit Cloud)

Frontend connects to deployed backend:
API_URL = "https://titanic-backend-klbp.onrender.com/chat"

---

# 🧪 Example Queries

## Deterministic Queries

- How many third class passengers survived?  
- What percentage of passengers were male?  
- How many passengers embarked from each port?  
- What was the average Fare?  
- Which class had the highest survival rate?  

## Visualization Queries

- Show histogram of Age  
- Scatter plot of Fare vs Age  
- Pie chart of Embarked  
- Bar chart of Pclass  

## LLM Queries

- Were women treated better?  
- Find correlation between fare and survival  
- Compare survival across social classes  

---

# ⚙️ Local Setup

## Clone
git clone https://github.com/diwyanshu6/titanic_ai.git

## Install

cd titanic_ai
pip install -r requirements.txt

## Run Backend


uvicorn backend.main:app --reload

## Run Frontend
streamlit run frontend/app.py


---

# 🎯 Design Philosophy

This project demonstrates:

- Hybrid AI architecture  
- Deterministic-first system design  
- Production-safe LLM integration  
- Modular backend structure  
- Logging-driven debugging  
- Cloud deployment workflow  
- Error-resilient API design  

---

# 📈 Future Improvements

- Query caching  
- Automated testing suite  
- Swagger documentation enhancement  
- Query history storage  
- Advanced NLP preprocessing  
- Dockerization  

---

# 🧠 What This Project Demonstrates

✔ Backend system design  
✔ AI routing architecture  
✔ Hallucination mitigation strategy  
✔ Cloud deployment workflow  
✔ Production logging  
✔ LLM safety management  
✔ Real-world debugging  

---

# 👤 Author

Diwyanshu  
AI Systems & Backend Engineering  

---


