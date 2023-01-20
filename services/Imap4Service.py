import email
from enum import Enum
import imaplib
import os
#from services import *
#from services import ReferenceEmail
import yaml

from ReferenceEmail import ReferenceEmail



class Imap4Service():
    def __init__(self):
        self.emails = []                
        self.email_list = []
        self.mail_server = None

    def retrieve_email_reference(self, groupBy = 1):    
        self.connect_to_server()

        if(groupBy == GroupBy.ByNone.value):
            self.retrieve_email_reference_groupby_none()
        if (groupBy == GroupBy.ByDate.value):
            self.retrieve_email_reference_groupby_date()
        elif (groupBy == GroupBy.ByTag.value):
            self.retrieve_email_reference_groupby_tag()
        elif (groupBy == GroupBy.ByTagAndDate.value):
            self.retrieve_email_reference_groupby_tag_and_date()
        
        self.write_md_file()
        self.server_disconnect() 
        
    def server_disconnect(self):
        self.mail_server.close()
        self.mail_server.logout()

    def connect_to_server(self,retrieve_from_folder="Filtering",search_by='SUBJECT "Filter"'):
        self.mail_server = imaplib.IMAP4_SSL('outlook.office365.com')        
        with open("settings.yml", "r") as f:
            config = yaml.safe_load(f)
        self.mail_server.login(config['login']['username'], config['login']['password'])
        self.mail_server.select(retrieve_from_folder) # can be "INBOX" also
        typ, folders = self.mail_server.list()
        status, emails = self.mail_server.search(None, search_by) # can be ALL also        
        self.email_ids = emails[0].split()
        
                 
    
    # def retrieve_email_reference(self):
        
                
    #     # Iterate through the list of email IDs and retrieve the email
    #     for email_id in self.email_ids:
    #         status, msg = self.mail_server.fetch(email_id,'(RFC822)')
    #         if status == 'OK':                
    #             msg = email.message_from_bytes(msg[0][1])                    
    #             try:
    #                 body = msg._payload[0]._payload.replace(os.linesep,"").rstrip("Get Outlook for iOS<https://aka.ms/o0ukef>")
    #             except:
    #                 body = f'Not able to get email payload in {email_id} with details,subject: {msg["Subject"]} , Date: {msg["Date"]}'
    #                 pass
    #             self.emails.append(ReferenceEmail(msg["Subject"],msg["Date"],body))
                
    #             #TODO: log this error instead
    #             print(f'Subject: {msg["Subject"]} , Date: {msg["Date"]} ')
    #             print(f'From: {msg["From"]}, ')                                
    #             print(f'Body: {body}')
                
                
                
    def retrieve_email_reference_groupby_none(self):        
        for email_id in self.email_ids:
            status, msg = self.mail_server.fetch(email_id,'(RFC822)')
            if status == 'OK':                
                msg = email.message_from_bytes(msg[0][1])                    
                try:
                    # body = msg._payload[0]._payload.replace(os.linesep,"").rstrip(os.linesep+"Get Outlook for iOS<https://aka.ms/o0ukef>"+os.linesep+)
                    body = msg._payload[0]._payload.rstrip(os.linesep+"Get Outlook for iOS<https://aka.ms/o0ukef>"+os.linesep)
                except:
                    body = f'Not able to get email payload in {email_id} with details,subject: {msg["Subject"]} , Date: {msg["Date"]}'
                    pass
                self.emails.append(ReferenceEmail(msg["Subject"],msg["Date"],body))
                
                #TODO: log this error instead
                print(f'Subject: {msg["Subject"]} , Date: {msg["Date"]} ')
                print(f'From: {msg["From"]}, ')                                
                print(f'Body: {body}')
               
                
    
    def retrieve_email_reference_groupby_date(self):
        pass        
    def retrieve_email_reference_groupby_tag(self):
        pass
    def retrieve_email_reference_groupby_tag_and_date(self):
        pass    
    
    def write_md_file(self, file_path="C:/", file_name="filtered.md"):        
        count = 1
        with open(os.path.join(file_path,file_name),"a") as file:
            for email_item in self.emails:                
                row = f'{count}. [ ] {email_item.content}, {email_item.date}'            
                row += os.linesep
                file.write(row)
                count+=1   

class GroupBy(Enum):
    ByNone = 1    
    ByDate = 2    
    ByTag = 3
    ByTagAndDate = 4