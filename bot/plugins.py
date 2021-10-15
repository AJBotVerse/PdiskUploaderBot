#!/usr/bin/env python3


'''Impoting Libraries and Modules'''
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import exceptions, UserNotParticipant
from pymongo import MongoClient
import __main__
from os import path
from inspect import currentframe
from bot.creds import *
from bot.messages import *


'''Connecting To Database'''
if connection_string:
    mongo_client = MongoClient(connection_string)
    db_user = mongo_client['Pdisk_Uploader']
    collection_user = db_user['members']


'''Defining Some Functions'''
#Function to find error in which file and in which line
def line_number():
    cf = currentframe()
    return f'In File {path.basename(__main__.__file__)} at line {cf.f_back.f_lineno}'

#Checking User whether he joined channel and group or not joined.
async def search_user_in_community(client, message):
    try:
        await client.get_chat_member('@AJPyroVerse', message.chat.id)
        await client.get_chat_member('@AJPyroVerseGroup', message.chat.id)
    except UserNotParticipant:
        await message.reply_text(not_joined_community, parse_mode = 'html',reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Join our Channel.',url = 'https://t.me/AJPyroVerse')],
        [InlineKeyboardButton('Join our Group.',url = 'https://t.me/AJPyroVerseGroup')]
        ]))
        return
    except exceptions.bad_request_400.ChatAdminRequired:
        return True
    except Exception as e:
        print(line_number(), e)
        return True
    else:
        return True

#Finding user in database, if not found then adding him
def checking_user_in_db(userid):
    if connection_string:
        document = {'userid' : userid}
        if collection_user.find_one(document):
            return True
        collection_user.insert_one(document)
    return

