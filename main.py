import imaplib
import email
import os
import yaml

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
typ, folders = mail.list()

mail.select('Filtering')

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
        body = msg._payload[0]._payload.rstrip("\r\n\r\n\r\nGet Outlook for iOS<https://aka.ms/o0ukef>")
        emails.append(EmailContent(msg["Subject"],msg["Date"],body))
        # Print the subject and sender of the email
        # print(f'Subject: {msg["Subject"]} , Date: {msg["Date"]} ')
        # #print(f'From: {msg["From"]}, ')
        # body = 
        # print(f'Msg: {body}')

# Close the mailbox and logout
mail.close()
mail.logout()

#write .md file
kms_path = "C:/"
filename = "filters.md"
count = 1

with open(os.path.join(kms_path,filename),"a") as file:
    for email in emails:
        file.write(f'{count}. [ ] {email.content} , {email.date}')
        count+=1
