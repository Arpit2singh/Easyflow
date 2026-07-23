# intake_agent/main.py

import tempfile
import os 
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import File , UploadFile 
from typing import List
import requests
import tempfile
import cv2
from intake_agent.vision_utils import image_process
import base64

load_dotenv() 


client = OpenAI(
     api_key = os.getenv("OPENAI_API_KEY") ,
     base_url="https://api.groq.com/openai/v1" 
)

system_instruction = "You are an agent that describes screenshots or images showing a user's technical issue. Describe what error, UI state, or problem is visible in plain text."

def data_from_bytes(bytes_data : List):
    frames_data = [] 
    
    for image_byte in bytes_data : 
        response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": [
                {"type": "text", "text": "Please get the important information of the bug from the image."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64.b64encode(image_byte).decode('utf-8')}"}}
            ]}
            ]
        )
        frames_data.append(response.choices[0].message.content)
    return frames_data
    
    
def extract_frame_from_path(video_path:str):
    cap = cv2.VideoCapture(video_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if length == 0 : 
        return [] 
    else : 
        frames = [] 
        positions = [length * 0.25, length * 0.5, length * 0.75]
        for i in positions:
            cap.set(cv2.CAP_PROP_POS_FRAMES , int(i)) 
            success , frame = cap.read() 
            
            if success:
                success2 , buffer = cv2.imencode(".png" , frame)
                if(success2):
                    frames.append(buffer.tobytes()) 
                    
        cap.release() 
        return frames           
                    
                    







def video_process(video_link : str):
    video_data = []
    parts = video_link.split("/")
    file_id = parts[5]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url)
    
    with tempfile.NamedTemporaryFile(delete=False , suffix=".mp4") as tmp : 
        tmp.write(response.content)
        tmp_path = tmp.name
    frames = extract_frame_from_path(tmp_path) 
    video_data.extend(data_from_bytes(frames))
    os.remove(tmp_path) 
    
    return video_data
    
    
    