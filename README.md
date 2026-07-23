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

## 💬 Sample Inputs & Human-Like Responses

Below are realistic examples of human user inputs and system agent responses across key workflows:

### 1. Classification Agent (`POST /classify-ticket`)
* **User Input:**
  > "My dashboard keeps crashing whenever I try to export the monthly billing report PDF, and it keeps giving me an Internal Server Error 500."

* **Agent Response (JSON):**
  ```json
  {
    "ticket_id": "8f3b2c1a-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
    "category": "TECHNICAL_ISSUE",
    "priority": "high",
    "description": "Dashboard crash during monthly billing report PDF export due to server 500 error."
  }
  ```

---

### 2. Smart Workload Assignment Agent (`POST /assign-ticket`)
* **Input Payload:**
  ```json
  {
    "ticket_id": "8f3b2c1a-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
    "category": "TECHNICAL_ISSUE",
    "priority": "high",
    "description": "Dashboard crash during monthly billing report PDF export due to server 500 error."
  }
  ```

* **Agent Response (JSON):**
  ```json
  {
    "status": "success",
    "message": "ticket sent to agent",
    "assigned_agent_id": 4
  }
  ```

---

### 3. SLA Escalation Agent (`GET /run-scheduler`)
* **Trigger Event:**
  > Automated SLA monitor detects ticket `#8f3b2c1a-4e5f-6a7b-8c9d-0e1f2a3b4c5d` in `pending` status exceeding the 15-minute SLA threshold.

* **Agent Action & Response (JSON):**
  ```json
  {
    "status": "scheduler run successfully",
    "escalated_tickets": [
      {
        "ticket_id": "8f3b2c1a-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
        "subject": "Dashboard crash on PDF export",
        "old_status": "pending",
        "new_status": "escalated",
        "action": "Escalation notification triggered to lead supervisor"
      }
    ]
  }
  ```

---

### 4. Automated Response Agent (`POST /generate-response`)
* **User Input:**
  * **Subject:** `Payment failed but amount debited from account`
  * **Description:** `I tried renewing my premium subscription today. The checkout page showed an error, but the payment was debited from my bank account. Please check and resolve this.`

* **Agent Response:**
  > **Subject:** Re: Payment failed but amount debited from account  
  > **Body:**  
  > "Hello,  
  >  
  > Thank you for reaching out to Easyflow Support. We understand how concerning it is when a payment is debited without immediate confirmation.  
  >  
  > We have verified your transaction log. Your transaction is currently being processed by our billing gateway. If the payment was debited successfully, your premium subscription will be activated automatically within 1 to 2 hours. In case the transaction was dropped by the bank, the debited amount will be automatically refunded to your original payment method within 3–5 business days.  
  >  
  > Should you need further assistance, feel free to reply directly to this thread!"

---

### 5. Conversational Status Assistant (`POST /check-status`)
* **User Input:**
  > "Hey, can you give me an update on ticket #8f3b2c1a regarding my dashboard crash?"

* **Agent Response:**
  > "Hello! I looked up ticket **#8f3b2c1a** for you.  
  >   
  > * **Status:** In Progress  
  > * **Assigned Handler:** Engineering / DevOps Team (Agent ID: 4)  
  > * **Priority:** High  
  > * **Latest Update:** The team has identified an issue with the PDF export library and is deploying a hotfix. Expected resolution is within 2 hours."

---

### 6. Multimodal Intake Agent (`POST /intake`)
* **User Input:**
  * **Subject:** `UI layout broken on login screen`
  * **Description:** `I am unable to click the login button after the latest app update. I've attached a screenshot.`
  * **Attachment:** `login_error.png`

* **Agent Response (JSON):**
  ```json
  {
    "subject": "UI layout broken on login screen",
    "description": "I am unable to click the login button after the latest app update. I've attached a screenshot.",
    "attachment_type": "image",
    "result": {
      "detected_elements": ["Overlapping login button", "CSS offset alert: 404 assets missing"],
      "summary": "Visual analysis confirms login button rendering behind main hero card container."
    }
  }
  ```

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

