# intake_agent/vision_utils.py

import os 
from openai import OpenAI
from dotenv import load_dotenv 
from fastapi import File , UploadFile
from typing import List
import base64
load_dotenv() 

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
system_instruction = "You are an agent that describes screenshots or images showing a user's technical issue. Describe what error, UI state, or problem is visible in plain text."
def data(image : UploadFile):
    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role":"system" , "content":system_instruction},
            {"role":"user", "content":[
                {"type":"text" , "text":"Please extract the metadata from the image."},
                {"type":"image_url" , "image_url": {"url":f"data:image/png;base64,{base64.b64encode(image.file.read()).decode('utf-8')}"}}
            ]}
        ]
    )
    return response.choices[0].message.content 



def image_process(image_process : List[UploadFile] = File(...)):
    image_data=[]
    for image in image_process:
        image_data.append(data(image)) 
    return image_data
       
    

