import smtplib
from email.message import EmailMessage 
from db.schemas.email_schemas import email_list_schema 
from db.client import dbClient
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


email_subject = "CORDIAL SALUDO COLEGA" 
email_smtp = "smtp.gmail.com" 
email_password = os.getenv("PASSWORD")
sender_email_address = os.getenv("EMAIL")

for i in email_list_schema(dbClient.dev.oplog.rs.find()):
    receiver_email_address = i["email"]
    # Create an email message object 
    message = EmailMessage() 

    # Configure email headers 
    message['Subject'] = email_subject 
    message['From'] = sender_email_address 
    message['To'] = receiver_email_address 

    # Set email body text 
    #message.set_content("I hope you has a good day, now it's available the page rpcIDE for everyone!, are you ready for this? https://rpcide.vercel.app/") 

    message.set_content("RPCIDE its available now") 

    # Set smtp server and port 
    server = smtplib.SMTP(email_smtp, '587') 

    # Identify this client to the SMTP server 
    server.ehlo() 

    # Secure the SMTP connection 
    server.starttls() 

    # Login to email account 
    server.login(sender_email_address, email_password) 

    # Send email 
    server.send_message(message) 

    # Close connection to server 
print("Sucessfull process")
server.quit()

