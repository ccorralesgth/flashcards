from enum import Enum
import imaplib
import os
from ReferenceEmail import *
import yaml

class Imap4Service:
    def __init__(self):
        self.emails = []                
        self.email_list = []
        self.mail_server = None

    def retrieve_email_reference(self, groupBy=1):        
        if (groupBy == GroupBy.ByDate):
            return self.retrieve_email_reference_by_date();
        elif (groupBy == GroupBy.ByTag):
            return self.retrieve_email_reference_by_tag();
        elif (groupBy == GroupBy.ByTagAndDate):
            return self.retrieve_email_reference_by_tag_and_date();
        

    def connect_to_server(self,retrieve_from_folder="INBOX",search_by='ALL'):
        self.mail_server = imaplib.IMAP4_SSL('outlook.office365.com')        
        with open("settings.yml", "r") as f:
            config = yaml.safe_load(f)

        self.mail_server.login(config['login']['username'], config['login']['password'])       
        self.mail_server.select(retrieve_from_folder = "Filtering")
        typ, folders = self.mail_server.list()
        status, emails = self.mail_server.search(None, search_by='SUBJECT "Filter"')        
        self.email_ids = emails[0].split()
        
    def write_md_file(self, file_path="C:/", file_name="filtered.md"):        
        count = 1

        with open(os.path.join(file_path,file_name),"a") as file:
            for email in self.emails:                
                row = f'{count}. [ ] {email.content}, {email.date}'            
                row += os.linesep
                file.write(row)
                count+=1                
    
    def retrieve_email_reference(self):
        self.connect_to_server()
                
        # Iterate through the list of email IDs and retrieve the email
        for email_id in self.email_ids:
            status, msg = self.mail_server.fetch(email_id,'(RFC822)')
            if status == 'OK':                
                msg = self.mail_server.message_from_bytes(msg[0][1])                    
                try:
                    body = msg._payload[0]._payload.replace(os.linesep,"").rstrip("Get Outlook for iOS<https://aka.ms/o0ukef>")
                except:
                    body = f'Not able to get email payload in {email_id} with details,subject: {msg["Subject"]} , Date: {msg["Date"]}'
                    pass
                self.emails.append(ReferenceEmail(msg["Subject"],msg["Date"],body))
                
                #TODO: log this error instead
                print(f'Subject: {msg["Subject"]} , Date: {msg["Date"]} ')
                print(f'From: {msg["From"]}, ')                                
                print(f'Body: {body}')

                # Close the mailbox and logout
                self.mail_server.close().logout()
                #mail.logout()

    def retrieve_email_reference_groupby_none(self):
        # Iterate through the list of email IDs and retrieve the email
        for email_id in self.email_ids:
            status, msg = self.mail_server.fetch(email_id,'(RFC822)')
            if status == 'OK':                
                msg = self.mail_server.message_from_bytes(msg[0][1])                    
                try:
                    body = msg._payload[0]._payload.replace(os.linesep,"").rstrip("Get Outlook for iOS<https://aka.ms/o0ukef>")
                except:
                    body = f'Not able to get email payload in {email_id} with details,subject: {msg["Subject"]} , Date: {msg["Date"]}'
                    pass
                self.emails.append(ReferenceEmail(msg["Subject"],msg["Date"],body))
                
                #TODO: log this error instead
                print(f'Subject: {msg["Subject"]} , Date: {msg["Date"]} ')
                print(f'From: {msg["From"]}, ')                                
                print(f'Body: {body}')

                # Close the mailbox and logout
                self.mail_server.close().logout()
                #mail.logout()
        
    def retrieve_email_reference_by_tag(self):
        pass
    def retrieve_email_reference_by_tag_and_date(self):
        pass


class GroupBy(Enum):    
    ByDate = 1    
    ByTag = 2
    ByTagAndDate = 3