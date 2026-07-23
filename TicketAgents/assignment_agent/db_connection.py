import os
import chromadb 
from dotenv import load_dotenv 
from google.generativeai import genai 
from sqlmodel import Session ,SQLModel, create_engine

load_dotenv() 

database_url=os.getenv("DATABASE_URL")

engine=create_engine(database_url , echo=True)


def get_session():
    with Session(engine) as session :
        yield session
        
def create_db_connection():
    SQLModel.metadata.create_all(engine)       