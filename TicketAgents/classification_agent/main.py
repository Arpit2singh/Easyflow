
import os 
from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import google.generativeai as genai 
import uuid
load_dotenv() 


client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY") , 
    base_url="https://api.groq.com/openai/v1" 
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gen_embedding(text : str , task_type="retrieval_query"):
    embed = genai.embed_content(
        model="models/gemini-embedding-001" , 
        content=text,
        task_type=task_type 
    )
    return embed["embedding"]

chroma_client = chromadb.CloudClient(
    api_key=os.getenv("chroma_api_key"),
    tenant=os.getenv("chroma_tenant"),
    database=os.getenv("chroma_database")
)

def unique_keys():
    return str(uuid.uuid4())  

system_instruction = """ You are an expert in classifying product bugs based on user descriptions. 

You should analyze the user's problem and map it to one of the following categories. 
Always respond with the category name exactly as written below. 

Categories:
- UI_ISSUE 
- TECHNICAL_ISSUE
- FUNCTIONALITY_ISSUE 
- PERFORMANCE_ISSUE
- SECURITY_ISSUE

also classify them on priority based on there nature 
example low , moderate , high , critical 

 respond back in json format with key category , priority and description
 
"""

def classification(user_input : str):
    embed_response = gen_embedding(user_input) 
    collection = chroma_client.get_or_create_collection("Tickets")
    collection.add(
        documents=[user_input],
        embeddings=[embed_response],
        ids=[str(uuid.uuid4())],
        metadatas={"source" : "Ticket" }
    )
    context = collection.query(
        query_embeddings=[embed_response],
        n_results=1
    )
    
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b" , 
        messages = [
            {"role" : "system" , "content" : system_instruction} ,
            {"role" : "user" , "content" : user_input},
            {"role" : "user" , "content" : str(context)}
        ],
       
        response_format={"type" : "json_object"}
    )
    return response.choices[0].message.content 
     
    
     
     

