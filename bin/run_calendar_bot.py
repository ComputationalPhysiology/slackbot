#!/usr/bin/env python3
# coding: utf-8
import os
import sys
import yaml
from pathlib import Path
import argparse
import datetime

import scholar_bot


channels = {'comphy': 'CGGTT3GE6'}

def get_args():

    descr = "Get upcoming confencerces and events from the Comphy confencerce calendar"
    usage = ("python run_sholar_bot --post_to_slack")
    parser = argparse.ArgumentParser(description=descr, usage=usage, add_help=True)

    parser.add_argument('--post_to_slack', action='store_true', dest='post_to_slack',
                        help='Post message to slack')

    return parser



def main_func(args):


    message = scholar_bot.get_upcoming_conferences(N=10)
    print(message)
    if args['post_to_slack']:
        print('post to slack!')
        scholar_bot.post_to_slack(message, [channels['comphy'],])
    print("Success!")

if __name__ == "__main__":
    
    parser = get_args()
    args = vars(parser.parse_args())
    print(args)
    main_func(args)
