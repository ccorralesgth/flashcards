import imaplib
import email
import yaml

# Connect to the server
mail = imaplib.IMAP4_SSL('outlook.office365.com')

#read from setting file
with open("settings.yml", "r") as f:
    config = yaml.safe_load(f)

# Login to your account
mail.login(config['login']['username'], config['login']['password'])

# Select the mailbox you want to retrieve emails from
mail.select('INBOX')

# Search for emails
#status, emails = mail.search(None, 'ALL')
status, emails = mail.search(None, 'SUBJECT "filter"')

# Get the list of email IDs
email_ids = emails[0].split()

# Iterate through the list of email IDs and retrieve the email
for email_id in email_ids:
    status, msg = mail.fetch(email_id, '(RFC822)')
    if status == 'OK':
        # Parse the email
        msg = email.message_from_bytes(msg[0][1])

        # Print the subject and sender of the email
        print(f'Subject: {msg["Subject"]}')
        print(f'From: {msg["From"]}')

# Close the mailbox and logout
mail.close()
mail.logout()
