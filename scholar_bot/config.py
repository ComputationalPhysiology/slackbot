#!/usr/bin/env python3
# coding: utf-8

import configparser
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

here = os.path.abspath(os.path.dirname(__file__))
config = configparser.SafeConfigParser({'token': os.environ.get('SLACK_BOT_TOKEN', '')})
files = config.read([
    './scholarbot.ini',
    os.path.join(here, 'scholarbot.ini'),
    os.path.expanduser('~/scholarbot.ini'),
    os.path.expanduser('~/.scholarbot/config')])

SLACK_TOKEN = config.get(
    'SLACK_BOT_TOKEN', 'token')


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
token_file = os.path.expanduser('~/.scholarbot/token.pickle')
cred_file = os.path.expanduser('~/.scholarbot/credentials.json')
if os.path.exists(token_file):
    with open(token_file, 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            cred_file, SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open(token_file, 'wb') as token:
        pickle.dump(creds, token)
