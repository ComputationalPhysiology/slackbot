#!/usr/bin/env python3
# coding: utf-8
import os
import yaml
import datetime
from post_slack import post_to_slack
import scholar_bot

channels = {'comphy': 'CGGTT3GE6'}

def load_yaml_file(fname):
    
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            d = yaml.load(f)
    else:
        d = {}
    return d

def dump_yaml(data, fname):
    with open(fname, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    

def compute_todays_impact():

    # Import input data
    people = load_yaml_file('people.yml')

    # Load database
    history = load_yaml_file('history.yml')

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

    dump_yaml(history, 'history.yml')

    # Create output mesage
    message = []
    message += [f"Your impact today is {num_cites}. Well done!"]
    message += [f"Your h-index today is {h}. Awesome!"]
    message += [f"The all stars (most cited-per-year papers (all time)) are:"]
    for (title, cites) in all_stars:
        message += [f'{N_all_stars}: {title} ({cites:2.1f})']
        N_all_stars = N_all_stars - 1
    message += [f"\nThe rising stars (most cited-per-year papers not older than {max_years} years) are:"]
    for (title, cites) in rising_stars:
        message += [f'{N_rising_stars}: {title} ({cites:2.1f})']
        N_rising_stars = N_rising_stars - 1
    return "\n".join(message)

if __name__ == "__main__":
    message = compute_todays_impact()
    print(message)
    post_to_slack(message, [channels['comphy'],])
    print("Success!")
