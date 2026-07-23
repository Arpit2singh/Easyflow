import os 
import psycopg2
from dotenv import load_dotenv 
from openai import OpenAI 
from typing import Dict, Any, List, Optional
import json 
import google.generativeai as genai

load_dotenv()


conn = psycopg2.connect(os.getenv("DATABASE_URL"))
curr = conn.cursor()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_chat_sessions: Dict[str, Any] = {}


groq_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

system_instruction = """You are a friendly and helpful ticket status assistant for a customer support system.

Your job is to:
1. Answer questions about ticket status, details, and history
2. If ticket data is provided in the context, use it to give accurate answers
3. If no ticket data is found, politely tell the user and ask them to provide a valid ticket ID
4. Be concise but informative
5. Format your response in a clean, readable way

When ticket data is available, include: status, subject, category, priority, assigned agent, and timestamps.
"""


def get_ticket_status(ticket_id: str) -> Optional[Dict]:
    """Query the tickets table for a specific ticket's details."""
    try:
        curr.execute(
            """SELECT t.ticket_id, t.subject, t.description, t.category, t.priority, 
                      t.status, t.created_at, t.assigned_at, t.assigned_agent_id,
                      a.name as agent_name, a.department as agent_department
               FROM tickets t 
               LEFT JOIN agents a ON t.assigned_agent_id = a.agent_id
               WHERE t.ticket_id = %s""",
            (ticket_id,)
        )
        row = curr.fetchone()
        if row:
            return {
                "ticket_id": str(row[0]),
                "subject": row[1],
                "description": row[2],
                "category": row[3],
                "priority": row[4],
                "status": row[5],
                "created_at": str(row[6]) if row[6] else None,
                "assigned_at": str(row[7]) if row[7] else None,
                "assigned_agent_id": row[8],
                "agent_name": row[9],
                "agent_department": row[10]
            }
        return None
    except Exception as e:
        conn.rollback()
        print(f"DB error: {e}")
        return None


def get_all_tickets_by_status(status: str) -> List[Dict]:
    """Query tickets filtered by status."""
    try:
        curr.execute(
            "SELECT ticket_id, subject, priority, status, created_at FROM tickets WHERE status = %s",
            (status,)
        )
        rows = curr.fetchall()
        return [
            {
                "ticket_id": str(r[0]),
                "subject": r[1],
                "priority": r[2],
                "status": r[3],
                "created_at": str(r[4]) if r[4] else None
            }
            for r in rows
        ]
    except Exception as e:
        conn.rollback()
        print(f"DB error: {e}")
        return []


def _get_gemini_chat(session_id: str):
    """Get or create a Gemini chat session for persistent history."""
    if session_id not in _chat_sessions:
        model = genai.GenerativeModel("gemini-2.0-flash")
        _chat_sessions[session_id] = model.start_chat(history=[])
    return _chat_sessions[session_id]


def _save_to_gemini_history(session_id: str, user_msg: str, assistant_msg: str):
    """Save the conversation turn to Gemini chat for persistence."""
    chat = _get_gemini_chat(session_id)
    # Send user message and get Gemini's acknowledgment (we use this purely for history storage)
    try:
        chat.send_message(
            f"[HISTORY STORE] User said: {user_msg}\nAssistant replied: {assistant_msg}\nJust acknowledge with 'stored'."
        )
    except Exception as e:
        print(f"Gemini history save error: {e}")


def _get_chat_history(session_id: str) -> str:
    """Retrieve chat history from the Gemini session."""
    if session_id not in _chat_sessions:
        return ""
    
    chat = _get_gemini_chat(session_id)
    history_parts = []
    for msg in chat.history:
        role = msg.role
        text = msg.parts[0].text if msg.parts else ""
        if "[HISTORY STORE]" in text:
            # Extract the actual conversation from stored history
            history_parts.append(text.replace("[HISTORY STORE] ", ""))
    
    return "\n".join(history_parts[-10:])  # Keep last 10 turns


def _extract_ticket_id(message: str) -> Optional[str]:
    """Try to extract a ticket ID (UUID format) from the user's message."""
    import re
    uuid_pattern = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
    match = re.search(uuid_pattern, message)
    return match.group(0) if match else None


def _detect_status_query(message: str) -> Optional[str]:
    """Detect if user is asking about tickets by status."""
    msg_lower = message.lower()
    status_keywords = {
        "pending": "pending",
        "escalated": "escalated", 
        "assigned": "assigned",
        "open": "open",
        "closed": "closed",
        "resolved": "resolved"
    }
    for keyword, status in status_keywords.items():
        if keyword in msg_lower and ("show" in msg_lower or "list" in msg_lower or "all" in msg_lower or "how many" in msg_lower):
            return status
    return None


def chat(user_message: str, session_id: str = "default") -> Dict[str, Any]:
    """Main chat handler — queries DB, uses Groq for response, Gemini for history."""
    
  
    history = _get_chat_history(session_id)
    
  
    ticket_context = ""
    ticket_id = _extract_ticket_id(user_message)
    status_query = _detect_status_query(user_message)
    
    if ticket_id:
        ticket_data = get_ticket_status(ticket_id)
        if ticket_data:
            ticket_context = f"\n\nTicket data from database:\n{json.dumps(ticket_data, indent=2)}"
        else:
            ticket_context = f"\n\nNo ticket found with ID: {ticket_id}"
    
    elif status_query:
        tickets = get_all_tickets_by_status(status_query)
        if tickets:
            ticket_context = f"\n\nTickets with status '{status_query}':\n{json.dumps(tickets, indent=2)}"
        else:
            ticket_context = f"\n\nNo tickets found with status '{status_query}'"
    
  
    context = ""
    if history:
        context += f"\n\nPrevious conversation:\n{history}"
    context += ticket_context
    
  
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_instruction + context},
            {"role": "user", "content": user_message}
        ]
    )
    
    assistant_reply = response.choices[0].message.content
    
 
    _save_to_gemini_history(session_id, user_message, assistant_reply)
    
   
    result = {
        "response": assistant_reply,
        "session_id": session_id
    }
    
    if ticket_id and ticket_context:
        result["ticket_id_detected"] = ticket_id
    
    return result
