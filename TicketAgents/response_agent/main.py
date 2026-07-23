import os 
from dotenv import load_dotenv 
from openai import OpenAI 
from typing import Dict , Any , List 
import json 


system_instruction = """You are a customer support response and summary generator.

You will receive a ticket's subject and description. Based on this, generate two things:

1. customer_response: A polite, professional, empathetic message addressed directly to the customer. Acknowledge their issue, reassure them it is being handled, and avoid technical jargon.

2. internal_summary: A short, technical summary for the internal support team. Include: likely issue category, possible root cause (if inferable), and urgency level. Keep it brief and factual — no pleasantries.

Respond ONLY with valid JSON in this exact format, with no markdown formatting, no code fences, and no extra text before or after:
{
    "customer_response": "<string>",
    "internal_summary": "<string>"
}
"""

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY") ,
    base_url="https://api.groq.com/openai/v1"
)

def generate_response(ticket : Dict[str , Any]):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant" ,
        messages=[
            {"role" : "system" , "content" : system_instruction} ,
            {"role": "user" , "content" : str(ticket)} 
        ],
        response_format={"type" : "json_object"}
    )
    if response.choices[0].message.content:
        return json.loads(response.choices[0].message.content) 
    else: 
        return "No response generated" 
    