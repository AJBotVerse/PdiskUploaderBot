#!/usr/bin/env python3


'''Credentials'''

import os

api_id = os.environ["API_ID"]

api_hash = os.environ["API_HASH"]

bot_token = os.environ["BOT_TOKEN"]

pdisk_api = os.environ["PDISK_API"]

try:
    connection_string = os.environ["MONGO_CON_STRING"]
except KeyError:
    connection_string = None

