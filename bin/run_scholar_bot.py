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

def load_yaml_file(fname):

    if hasattr(yaml, 'FullLoader'):
        kwargs = dict(Loader=yaml.FullLoader)
    else:
        kwargs = {}
    
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            d = yaml.load(f, **kwargs)
    else:
        d = {}
    return d

def dump_yaml(data, fname):
    with open(fname, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    

def compute_todays_impact(history_file, people_file):

    # Import input data
    people = load_yaml_file(people_file)

    # Load database
    history = load_yaml_file(history_file)

    publications = scholar_bot.extract_scholar_publications(people)
   
    # Compute impact and h-index 
    num_cites = scholar_bot.impact(publications)
    h = scholar_bot.h_index(publications)
    
    # Find shooting star papers
    max_years = 5
    N_all_stars = 5
    N_rising_stars = 3
    all_stars = scholar_bot.all_stars(publications, N=N_all_stars)
    rising_stars = scholar_bot.rising_stars(publications, N=N_rising_stars, max_years=max_years)
    

    # Add new input to history and dump to database
    today = datetime.datetime.now().date().isoformat()
    history[today] = dict(num_cites=num_cites,
                          h_index=h,
                          all_stars=all_stars,
                          rising_stars=rising_stars)

    dump_yaml(history, history_file)

    # Create output mesage
    message = []
    message += [f"Your impact today is {num_cites}. Well done!"]
    message += [f"Your h-index today is {h}. Awesome!"]
    message += [f"*The all stars (most cited-per-year papers (all time)) are*:"]
    for (title, cites) in all_stars:
        message += [f'{N_all_stars}: {title} ({cites:2.1f})']
        N_all_stars = N_all_stars - 1
    message += [f"\n*The rising stars (most cited-per-year papers not older than {max_years} years) are*:"]
    for (title, cites) in rising_stars:
        message += [f'{N_rising_stars}: {title} ({cites:2.1f})']
        N_rising_stars = N_rising_stars - 1
    return "\n".join(message)

def get_args():

    descr = "Get citations from the Copmutational Physiology group"
    usage = ("python run_sholar_bot --history '~/.scholar_history.yml' "
             "--people '~/.comphy_people.yml' --post_to_slack")
    parser = argparse.ArgumentParser(description=descr, usage=usage, add_help=True)

    parser.add_argument('--history', action="store", dest="history",
                        default='~/.scholarbot/history.yml',
                        type=str, help="Where to store the history")
             
    parser.add_argument('--people', action="store", dest="people",
                        default='~/.scholarbot/people.yml',
                        type=str, help="Where to load the people")

    parser.add_argument('--post_to_slack', action='store_true', dest='post_to_slack',
                        help='Post message to slack')

    return parser



def main_func(args):

    history_file = Path(os.path.expanduser(args['history']))
    history_file.parent.mkdir(parents=True, exist_ok=True)

    people_file = Path(os.path.expanduser(args['people']))

    if not people_file.is_file():
        print(f'No peoople found in {people_file}')
        sys.exit()

    message = compute_todays_impact(history_file, people_file)
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
