#!/usr/bin/env python3


'''Credentials'''

import os

bot_token = os.environ["BOT_TOKEN"]

api_id = os.environ["API_ID"]

api_hash = os.environ["API_HASH"]

pdisk_api = os.environ["PDISK_API"]

try:
    connection_string = os.environ["MONGO_CON_STRING"]
except KeyError:
    connection_string = None

