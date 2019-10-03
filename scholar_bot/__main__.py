#!/usr/bin/env python3
"""Slackbot for ComPhy

Available arguments
-------------------
All these arguments can be called with '-h' or '--help' to see the
additional options

    post_message
        Post message

    conferences
        Post upcoming conferences

    impact
        Post impact


Available options
-----------------

    -h, --help      Show this help
    -v, --version   Show version number


Contact
-------
Henrik Finsberg (henriknf@simula.no)

"""
__author__ = "Henrik Finsberg (henriknf@simula.no), 2017--2019"
__maintainer__ = "Henrik Finsberg"
__email__ = "henriknf@simula.no"

import sys
import os
from pathlib import Path
import scholar_bot

channels = {"comphy": "CGGTT3GE6"}


def main():
    """
    Main execution of the mps package
    """

    if len(sys.argv) < 2:
        print(__doc__)
        return

    # Show help message
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(__doc__)

    elif sys.argv[1] == "-v" or sys.argv[1] == "--version":
        from . import __version__

        print(__version__)

    elif sys.argv[1] == "post_message":
        message = sys.argv[2]
        scholar_bot.post_to_slack(message, [channels["comphy"]])

    elif sys.argv[1] == "conferences":
        message = scholar_bot.get_upcoming_conferences(N=10)
        print(message)
        print("post to slack!")
        scholar_bot.post_to_slack(message, [channels["comphy"]])
        print("Success!")

    elif sys.argv[1] == "impact":
        history_file = Path(os.path.expanduser("~/.scholarbot/history.yml"))
        history_file.parent.mkdir(parents=True, exist_ok=True)

        people_file = Path(os.path.expanduser("~/.scholarbot/people.yml"))

        if not people_file.is_file():
            print(f"No peoople found in {people_file}")
            sys.exit()

        message = scholar_bot.compute_todays_impact(history_file, people_file)
        print(message)
        scholar_bot.post_to_slack(message, [channels["comphy"]])
        print("Success!")

        raise NotImplementedError

    else:
        print("Argument {} not recongnized".format(sys.argv[1]))
        print(__doc__)


if __name__ == "__main__":
    main()
