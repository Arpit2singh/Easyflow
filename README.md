# Easyflow - Smart Multi-Agent Ticketing System

**Easyflow** is an intelligent, automated ticketing workflow system powered by specialized AI micro-agents built on FastAPI. Designed for modern enterprise support, Easyflow streamlines end-to-end customer support operations—from multimodal intake and intelligent classification to automated assignment, SLA monitoring, and response generation.

---

## 🤖 Agent Ecosystem Overview

Easyflow breaks down support ticketing into dedicated, autonomous AI agents located under `TicketAgents/`:

| Agent | Module | Description & Role |
| :--- | :--- | :--- |
| **Intake Agent** | `intake_agent/` | **Multimodal Data Processing**: Handles rich media uploads (images and video URLs/frames), analyzing visuals to extract actionable ticket context. |
| **Classification Agent** | `classification_agent/` | **Intelligent Categorization**: Evaluates ticket content to assign priority levels, urgency tags, problem categories, and sentiment scoring. |
| **Assignment Agent** | `assignment_agent/` | **Smart Workload Routing**: Dynamically assesses agent workloads and skill sets to route tickets to the optimal human or AI handler. |
| **Escalation Agent** | `escalation_agent/` | **SLA & Breach Tracking**: Monitors open tickets against resolution SLAs, triggering automated escalations for pending or high-risk issues. |
| **Response Agent** | `response_agent/` | **Automated Draft Synthesis**: Generates accurate, context-aware draft responses and proposed action plans for tickets. |
| **Status Check Agent** | `status_check_agent/` | **Conversational Assistant**: Enables users and support teams to query real-time ticket status through a conversational interface with session history. |

---

## 🚀 FastAPI Backend Endpoints (`TicketAgents/server.py`)

The unified FastAPI server exposes key REST endpoints for agent operations:

* `POST /intake` — Processes image-based ticket attachments.
* `POST /intake-video` — Processes video links and extracts frames for ticketing context.
* `POST /classify-ticket` — Runs the classification pipeline to score priority, tags, and assign a unique `ticket_id`.
* `POST /assign-ticket` — Evaluates handler workloads and assigns the ticket.
* `GET /run-scheduler` — Triggers SLA checks and escalations via the Escalation Agent.
* `POST /generate-response` — Generates AI response suggestions for open tickets.
* `POST /check-status` — Conversational chat endpoint to ask questions about ticket resolution status.
* `GET /ticket-status/{ticket_id}` — Fetches direct status metadata for a specific ticket.

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.9+
- Pip package manager

### 2. Environment Setup
Create a `.env` file inside the `TicketAgents/` folder (or workspace root) for your local environment configuration:

```env
# Local Environment Configuration (DO NOT COMMIT SECRETS)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=your_database_connection_string
```

> **Note**: `.env` files are excluded via `.gitignore` to prevent sensitive keys from being committed.

### 3. Installation & Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Launch FastAPI backend server
uvicorn TicketAgents.server:app --reload
```

Server will run on `http://127.0.0.1:8000` with interactive API docs available at `http://127.0.0.1:8000/docs`.

---

## 🔐 Security & Configuration
All credentials, API keys, and sensitive environment configs MUST remain in local `.env` files. The `.gitignore` configuration strictly ignores `.env`, virtual environments (`venv/`), and compiled caches.
