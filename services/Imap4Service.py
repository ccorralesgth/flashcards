import email
from enum import Enum
import imaplib
import os
#from services import *
#from services import ReferenceEmail
import yaml
from datetime import datetime
from dateutil import parser

from ReferenceEmail import ReferenceEmail



class Imap4Service():
    def __init__(self):
        self.emails = []                
        self.email_list = []
        self.mail_server = None
        self.username = ""
        self.password = ""
        self.file_path = ""
        self.file_name = ""
        self.load_configurations()

    def load_configurations(self):
        with open("settings.yml","r") as f:
            config = yaml.safe_load(f)
        
        self.username = config['login']['username']
        self.password = config['login']['password']
        self.file_path = config['generatefile']['filepath']
        self.file_name = config['generatefile']['filename']

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
        # with open("settings.yml", "r") as f:
        #     config = yaml.safe_load(f)
        # self.mail_server.login(config['login']['username'], config['login']['password'])
        self.mail_server.login(self.username, self.password)
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
                #msg = email.message_from_bytes(msg[0][1])                    
                try:
                    if(isinstance(email.message_from_bytes(msg[0][1])._payload[0],email.message.Message)):
                        body_url = email.message_from_bytes(msg[0][1])._payload[0]._payload.replace(os.linesep,'').rstrip("Get Outlook for iOS<https://aka.ms/o0ukef>")
                        dateformated  = parser.parse(email.message_from_bytes(msg[0][1])["Date"]).strftime('%c')
                    else:
                        body_url = ''
                    # body = msg._payload[0]._payload.replace(os.linesep,"").rstrip(os.linesep+"Get Outlook for iOS<https://aka.ms/o0ukef>"+os.linesep+)
                    
                    self.emails.append(ReferenceEmail(email.message_from_bytes(msg[0][1])["Subject"],dateformated,body_url))

                    #TODO: log this error instead
                    print(f'Subject: {email.message_from_bytes(msg[0][1])["Subject"]} , Date: {dateformated}')
                    print(f'From: {email.message_from_bytes(msg[0][1])["From"]}, ')                                
                    print(f'Body: {body_url}')
                except ValueError as ve1:
                    print('ValueError 1:', ve1)
                    body = f'Not able to get email payload in {email_id} with details,subject: {email.message_from_bytes(msg[0][1])["Subject"]} , Date: {dateformated}'                    
    
    def retrieve_email_reference_groupby_date(self):
        pass        
    def retrieve_email_reference_groupby_tag(self):
        pass
    def retrieve_email_reference_groupby_tag_and_date(self):
        pass    
    
    def write_md_file(self):        
        count = 1
        with open(os.path.join(self.file_path,self.file_name),"w") as file:
            for email_item in self.emails:      
                try: 
                    if (email_item.url != ''):
                        row = f'{count}. [ ] {email_item.url}, {email_item.date}'            
                        row += os.linesep
                        file.write(row)
                        count+=1   
                except:
                    print(f"error accessing email data: {count}")
        
        #print(f"file {str.join(self.file_name,self.file_name)} ")

                

class GroupBy(Enum):
    ByNone = 1    
    ByDate = 2    
    ByTag = 3
    ByTagAndDate = 4