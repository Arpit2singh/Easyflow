import psycopg2
import os 
from dotenv import load_dotenv
from datetime import datetime ,timedelta
from typing import Dict , Any , List 
from apscheduler.schedulers.background import BackgroundScheduler 


load_dotenv()


scheduler = BackgroundScheduler()




conn = psycopg2.connect(os.getenv("DATABASE_URL"))
curr = conn.cursor()

SLA_MINUTES=15

def check_escalation():
    now = datetime.now() 
    response = curr.execute(f"""
                            select ticket_id ,subject from tickets where status = 'pending' and now() - created_at > INTERVAL '{SLA_MINUTES} minute'
                            """)
    querygo = curr.fetchall()

    set_escalation = curr.execute(f"""update tickets set status = 'escalated' where status = 'pending' and now() - created_at > INTERVAL '{SLA_MINUTES} minute' """)


    conn.commit()
    if querygo:
        print(f"escalated ticket {querygo}")
        for ticket_id , subject in querygo:
            notify_escalation(ticket_id)
    else: 
        print("no escalation")
        
def notify_escalation(ticket_id) : 
    print(f"notifyng for escalation {ticket_id}")        
    return False 

scheduler.add_job(check_escalation , trigger='interval' ,minutes=1 )

scheduler.start() 
check_escalation() 