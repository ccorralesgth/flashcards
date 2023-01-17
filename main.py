from services.Imap4Service import Imap4Service

if __name__ == '__main__':    
    emil_service = Imap4Service()
    emil_service.retrieve_email_reference()
