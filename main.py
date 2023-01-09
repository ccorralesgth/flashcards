import imaplib
import email
import os
import string
import yaml
import re

class EmailContent:  
    def __init__(self, title, date, content):
        self.title = title
        self.date = date
        self.content = content
    
    
# Connect to the server
mail = imaplib.IMAP4_SSL('outlook.office365.com')

#read from setting file
with open("settings.yml", "r") as f:
    config = yaml.safe_load(f)

# Login to your account
mail.login(config['login']['username'], config['login']['password'])

# Select the mailbox you want to retrieve emails from
#mail.select('INBOX')

mail.select('Filtering')

typ, folders = mail.list()

# Search for emails
#status, emails = mail.search(None, 'ALL')
status, emails = mail.search(None, 'SUBJECT "filter"')

# Get the list of email IDs
email_ids = emails[0].split()

emails = []

# Iterate through the list of email IDs and retrieve the email
for email_id in email_ids:
    status, msg = mail.fetch(email_id, '(RFC822)')
    if status == 'OK':
        # Parse the email
        msg = email.message_from_bytes(msg[0][1])    
        #msg = email.message_from_string(msg[0][1]) 
        try:
            body = msg._payload[0]._payload.replace(os.linesep,"").rstrip("Get Outlook for iOS<https://aka.ms/o0ukef>")
            
            #body = body.replace()
            #body = re.sub(r"\s+", " ", body)
            #body = string.strip(body)            
            #body = body.replace(os.linesep,"")

        except:
            body = f'Not able to find payload in {email_id} with details,subject: {msg["Subject"]} , Date: {msg["Date"]}'
            pass
        emails.append(EmailContent(msg["Subject"],msg["Date"],body))
        #Print the subject and sender of the email
        print(f'Subject: {msg["Subject"]} , Date: {msg["Date"]} ')
        print(f'From: {msg["From"]}, ')
        
        #print(f'Body: {msg.get_payload(decode=True).decode()}')
        #print(f'Body: {msg.get_payload().decode}')
        print(f'Body: {body}')

# Close the mailbox and logout
mail.close()
mail.logout()

#write .md file
kms_path = "C:/"
filename = "filtered.md"
count = 1

with open(os.path.join(kms_path,filename),"a") as file:
    for email in emails:
        #todo group by dates += os.linesep
        row = f'{count}. [ ] {email.content}, {email.date}'
       # row.remo
        row += os.linesep
        file.write(row)
        count+=1
