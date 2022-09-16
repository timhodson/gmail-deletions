from __future__ import print_function
import datetime

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']
credentials_file = '/Users/timhodson/Documents/client_secret_14606609586-u229ommum45s662toqjpnhmkjj0b07sj.apps.googleusercontent.com.json'
label_id = 'Label_2'

def log_message(message):
    # log message showing elapsed time since last log message
    date_stamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print("\t".join([date_stamp, message]))

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    log_message('Get Credentials')
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        log_message('Get Gmail Service')
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # The label I am interested in has an id 'Label_2'
        # I got this by running the 'quickstart.py' script and looking at the output.
        # 500 seems to be the maximum we can get at once
        request = service.users().messages().list(userId='me', labelIds=label_id, maxResults=500)
        results = request.execute()
        messages = results.get('messages', [])

        while results.get('nextPageToken'):
            log_message("Getting messages... {} ({})".format(len(messages),results.get('nextPageToken')))
            request = service.users().messages().list_next(request, results)
            results = request.execute()
            messages.extend(results.get('messages', []))

        if not messages:
            log_message('No messages found.')
            return

        # how many messages did we have?
        log_message('Got messages: {}'.format(len(messages)))

        # before deleting the messages you could take a look at them all - but that might take some time...
        # for message in messages:
        #     print("=== {} ===".format(message['id']))
        #     message_detail = service.users().messages().get(userId='me', id=message['id']).execute()
        #     print("{}".format(message_detail['snippet']))

        def divide_chunks(l, n):
            # looping till length l
            for i in range(0, len(l), n):
                yield l[i:i + n]
        
        # extract the ids from messages
        message_ids = [message['id'] for message in messages]

        chunks = divide_chunks(message_ids, 500)

        # delete the messages
        for idx, chunk in enumerate(chunks):
            deletion_body = {'ids': chunk}
            # print("{}".format(chunk))
            log_message("Deleting messages...{}:{}".format(idx,len(chunk)))
            # service.users().messages().batchDelete(userId='me', body=deletion_body).execute()

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()