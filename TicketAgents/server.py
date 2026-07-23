import uuid
from fastapi import FastAPI , UploadFile , File , Body ,Form
from typing import List 
from intake_agent.vision_utils import image_process 
from intake_agent.video_utils import video_process , data_from_bytes
from classification_agent.main import classification 
import json
from pydantic import BaseModel
from assignment_agent.main import load_handler 
from typing import Any
from escalation_agent.main import check_escalation
from response_agent.main import generate_response
from status_check_agent.main import chat as status_chat, get_ticket_status

class ClassificationResponse(BaseModel):
    user_input : str 
 
class TicketInput(BaseModel):
    subject :str 
    description : str 

class ChatInput(BaseModel):
    message : str 
    session_id : str = "default"

app = FastAPI() 
@app.get("/")
def root():
    return "server is running" 

@app.post("/intake")
def intake_image(subject : str = Form(...) , description : str = Form(...) , image_file : List[UploadFile] = File(...)):
         result = image_process(image_file) 
         return {
             "subject" : subject,
             "description" : description,
             "attachment_type" : "image", 
             "result" : result
         }
         
@app.post("/intake-video")    
def intake_video(subject : str = Form(...) , description : str = Form(...) , video_link: str = Form(...)):
    result = video_process(video_link)
  
    return {
        "subject":subject,
        "description":description,
        "attachment_type" : "video",
        "result" : result
    }   
    
    
@app.post("/classify-ticket")
def classify_ticket(request : ClassificationResponse):
    response = classification(request.user_input) 
    response = json.loads(response)
    ticket_id = uuid.uuid4()
    response["ticket_id"] = str(ticket_id) 
    
    return response


@app.post("/assign-ticket")
def assign_ticket(ticket : dict): 
    result = load_handler(ticket) 
    return result 
    
@app.get("/run-scheduler")
def run_scheduler():
    check_escalation() 
    return {"status" : "scheduler run successfully"}    


@app.post("/generate-response")
def generate_resposne(ticket : TicketInput):
    resposne = generate_response(ticket.dict())
    return resposne

@app.post("/check-status")
def check_status(chat_input : ChatInput):
    result = status_chat(chat_input.message, chat_input.session_id)
    return result

@app.get("/ticket-status/{ticket_id}")
def ticket_status(ticket_id : str):
    data = get_ticket_status(ticket_id)
    if data:
        return data 
    return {"error": "Ticket not found"}