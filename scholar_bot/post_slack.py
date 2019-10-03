#!/usr/bin/env python3
# coding: utf-8
import slack

from .config import SLACK_TOKEN


class SlackPoster:
    def __init__(self, token, channels):
        self.client = slack.WebClient(token=token)
        self.channels = channels

    def post(self, message):
        for ch in self.channels:
            self.client.chat_postMessage(
                channel=ch, text=message, as_user=False, username="scholarbot"
            )


_poster = None


def post_to_slack(message, channels):
    global _poster
    if _poster is None:
        _poster = SlackPoster(SLACK_TOKEN, channels)
    _poster.post(message)
