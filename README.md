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
python3 -m virtualenv venv
source venv/bin/activate
```

install the dependencies
```
pip install -r requirements.txt
```

and install the bot
```
python setup.py install
```

## Running the bot

You can run the bot using the script
```
run_scholar_bot.py
```
To see how to run it do
```
run_scholar_bot.py --help
```

To actually post messages on Slack you need to pass the flag `--post_to_slack`
Please consult the [Slack API](https://api.slack.com) for how to set
up the bot. You can set you secret token either as an environment
varialbe (`SLACK_BOT_TOKEN`) or in a config file. I have mine in a
folder `~/scholarbot/config` and it looks like this:

```
[SLACK_BOT_TOKEN]
token = put your secret token here
```

I also have the `people.yml` file (which you will find in this repo as
well) in the same folder.

## Scheduling the bot
If you want your bot to e.g post a message on slack say one time evey
week, then you set up a cron job to do this. Check out [this
video](https://youtu.be/QZJ1drMQz1A) by Corey Schafer which explains
this very well.
