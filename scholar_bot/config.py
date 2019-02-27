#!/usr/bin/env python3
# coding: utf-8

import configparser
import os

here = os.path.abspath(os.path.dirname(__file__))
config = configparser.SafeConfigParser({'token': os.environ.get('SLACK_BOT_TOKEN', '')})
files = config.read([
    './scholarbot.ini',
    os.path.join(here, 'scholarbot.ini'),
    os.path.expanduser('~/scholarbot.ini'),
    os.path.expanduser('~/.scholarbot/config')])

SLACK_TOKEN = config.get(
    'SLACK_BOT_TOKEN', 'token')
