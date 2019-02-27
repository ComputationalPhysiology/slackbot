# ScholarBot

This is the Slack bot used to post updates about citations for the
Computational Phyisoligy department at Simula.
The ScholarBot is highly inspired by the
[impact_bot](https://github.com/meg-simula/impact-bot), but is based
only one python (as opposed to the `impact_bot` which uses an
R-package.

## Installation
You need python >= 3.6.
Create a virtual environment
```
python -m virtualenv venv
source venv/bin/activate
```

install the dependencies
```
pip install -r requirements.txt
```

And run the bot
```
python run_scholar_bot.py
```

Please consult the [Slack API](https://api.slack.com) for how to set
up the bot.
