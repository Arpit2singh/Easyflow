import os
import chromadb 
from dotenv import load_dotenv 
# from google.generativeai import genai 
from sqlmodel import Session ,SQLModel, create_engine
import psycopg2
from typing import Dict , List , Any
from openai import OpenAI
import json
from datetime import datetime 
load_dotenv() 


conn = psycopg2.connect(os.getenv('DATABASE_URL'))

curr = conn.cursor()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_agent",
            "description": "Fetch all agents with their capacity and load",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_ticket",
            "description": "Send the ticket to a chosen agent",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "integer"},
                    "ticket": {"type": "object"}
                },
                "required": ["agent_id", "ticket"]
            }
        }
    }
]
system_instruction_getAgent= """ you are the agent finder which will get the agents based on the ticket and there capacity and max capacity you have the agents data in context 
so make the best possible agent for the ticket """

def get_agent(ticket : Dict[str , Any]):
    query = "select * from agents"    
    curr.execute(query)
    context = curr.fetchall()
    
    client = OpenAI(
        api_key = os.getenv("OPENAI_API_KEY") ,
        base_url="https://api.groq.com/openai/v1" 
    )
    
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b" ,
        messages = [
            {"role" : "system" , "content" : system_instruction_getAgent},
            {"role" : "user" , "content" : str(ticket)},
            {"role" : "user" , "content" : str(context)}
        ],
      
    )
    if response : return response.choices[0].message.content
    else : return "Agent not found"
    
system_instruction_sendTicket= """  you are the agent sender which will send the ticket to the agent you can use the available agents list to send the ticket choose wisely which is the best option main goal load balance
after completion give the name of the user and there employee id 
""" 

def send_ticket(ticket: Dict, agent_id: int):
   
    curr.execute(
        "UPDATE tickets SET assigned_agent_id = %s, status = %s, assigned_at = %s WHERE ticket_id = %s",
        (agent_id, "assigned", datetime.now(), ticket["ticket_id"])
    )
  
    curr.execute(
        "UPDATE agents SET current_load = current_load + 1 WHERE agent_id = %s",
        (agent_id,)
    )
    conn.commit()
    return {"status": "success", "message": "ticket sent to agent"}




system_instruction=""" You are the agent assigner you have the access of the 2 tools and the ticket
1. Get Agents (tool)
2. Send Ticket (tool)
which assign the task based on category and priority """
system_instruction_sendTicket_forced = """You are the ticket sender. You have already received the agent selection data below.
Do NOT call get_agent again — that step is complete.
Your ONLY task now is to call the send_ticket tool with the correct agent_id extracted from the agent data provided.
"""
message_history=[]
    
def load_handler(ticket : Dict):
    
    client = OpenAI(
        api_key = os.getenv("OPENAI_API_KEY") ,
        base_url="https://api.groq.com/openai/v1" 
    )
    
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b" ,
        messages = [
            {"role" : "system" , "content" : system_instruction},
            {"role" : "user" , "content" : str(ticket)}
        ],
      
        tools=tools
    )
   
    msg = response.choices[0].message
    if msg == None : return "Agent 1 not found" 
    if msg.tool_calls and msg.tool_calls[0].function.name == "get_agent" :
        data = get_agent(ticket) 
        response_2 = client.chat.completions.create(
            model = "openai/gpt-oss-20b",
            messages = [
                {"role" : "system" , "content" : system_instruction_sendTicket_forced},
                {"role" : "user" , "content" : str(ticket)},
                {"role" : "user" , "content" : str(data)},
                {"role" : "user" , "content" : "get_agent"}
            ],
      
            tools=tools ,
            tool_choice={"type": "function", "function": {"name": "send_ticket"}}
        )   
        msg2 = response_2.choices[0].message 
        if msg2 == None : return "Agent 2 not found" 
        if msg2.tool_calls and msg2.tool_calls[0].function.name == "send_ticket" : 
            arguments = json.loads(msg2.tool_calls[0].function.arguments) 
            data = send_ticket(ticket , arguments["agent_id"]) 
            
            return data 
        
    