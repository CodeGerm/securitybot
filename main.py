#!/usr/bin/env python
import logging

from securitybot.bot import SecurityBot
from securitybot.chat.slack import Slack
from securitybot.tasker.sql_tasker import SQLTasker
from securitybot.auth.default import DefaultAuth
from securitybot.sql import init_sql
from os import getenv

import duo_client

CONFIG = {}
SLACK_KEY = getenv('SLACK_API_TOKEN', 'slack_api_token')
DUO_INTEGRATION = getenv('DUO_INTEGRATION_KEY', 'duo_integration_key')
DUO_SECRET = getenv('DUO_SECRET_KEY', 'duo_secret_key')
DUO_ENDPOINT = getenv('DUO_ENDPOINT', 'duo_endpoint')
REPORTING_CHANNEL = getenv('REPORTING_CHANNEL', 'some_slack_channel_id')
ICON_URL = 'https://s3-us-west-2.amazonaws.com/slack-files2/avatars/2016-12-07/113269613041_dfc5b7cb41ffd17b494d_48.png'

def init():
    # Setup logging
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s %(levelname)s] %(message)s')
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('usllib3').setLevel(logging.WARNING)

def main():
    init()
    init_sql()

    # Create components needed for Securitybot
    # duo_api = duo_client.Auth(
    #     ikey=DUO_INTEGRATION,
    #     skey=DUO_SECRET,
    #     host=DUO_ENDPOINT
    # )
    # duo_builder = lambda name: DuoAuth(duo_api, name)
    default_builder = lambda name: DefaultAuth(name)
    chat = Slack('YanlinBot', SLACK_KEY, ICON_URL)
    tasker = SQLTasker()

    sb = SecurityBot(chat, tasker, default_builder, REPORTING_CHANNEL, 'config/bot.yaml')
    sb.run()

if __name__ == '__main__':
    main()
