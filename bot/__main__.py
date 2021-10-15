#!/usr/bin/env python3


'''Impoting Libraries, Modules & Credentials'''
from pyrogram import Client, filters
from requests import head, post
from bot.plugins import *


'''Login as a Bot'''
bot = Client(
    'PdiskUploader',
    api_id = api_id,
    api_hash = api_hash,
    bot_token = bot_token
)


''''Defining Some Handlers for Bot'''
#Start Handler
@bot.on_message(filters.private & filters.command(["start"]))
async def start_handler(client, message):
    if await search_user_in_community(client, message):
        await message.reply_text(start_msg, parse_mode = 'html')
    return checking_user_in_db(message.chat.id)

#Help Handler
@bot.on_message(filters.command(["help"]))
async def help_handler(client, message):
    if await search_user_in_community(client, message):
        await message.reply_text(help_msg, parse_mode = 'html')
    return

#For Owner/Developer of Bot Only, Sent message to all Bot Users
@bot.on_message(filters.chat(1972357814) & filters.regex("^/broadcast(.+)"))
async def broadcast_handler(client, message):
    try:
        #Extracting Broadcasting Message
        message = message.text.split('/broadcast ')[1]
    except IndexError:
        await message.reply_text(broadcast_failed, parse_mode = 'html')
    except Exception as e:
        print(line_number(), e)
    else:
        #Getting User`s Id from Database
        for userid in [document['userid'] for document in collection_user.find()]:
            try:
                #Sending Message One By One
                await bot.send_message(userid, message)
            except exceptions.bad_request_400.UserIsBlocked:
                #User Blocked the bot
                collection_user.delete_one({'userid' : userid})
            except Exception as e:
                print(line_number(), e)
    return

#Uploading url containing Video to Pdisk
@bot.on_message(filters.private)
async def upload_handler(client, message):
    if message.entities:
        if await search_user_in_community(client, message):
            if message.entities[0].type == "url":
                splitted_msg = message.text.split(' ')
                if len(splitted_msg) == 2:
                    url, filename = splitted_msg
                    if head(url, allow_redirects=True).headers.get('content-length'):
                        link = f'http://linkapi.net/open/create_item?api_key={pdisk_api}&content_src={url}&link_type=link&title={filename}'
                        response = post(link)
                        if response.status_code == 200:
                            videoid = response.json()["data"]["item_id"]
                            await message.reply_text(f"<b>Your Video is successfully uploaded to Pdisk.</b>\nLink <code>https://pdisk.net/share-video?videoid={videoid}</code>\n\n<b>If this link shows '<i>File is not available</i>' then wait for few minutes and check it later.</b>", parse_mode = 'html')
                            return
                    await message.reply_text(unsuccessful_upload, parse_mode = 'html')
                    return
                else:
                    await message.reply_text(invalid_format_msg, parse_mode = 'html')
                    return
            elif message.media:
                await message.reply_text(media_msg, parse_mode = 'html')
    return
        

'''Bot is Started to run all time'''
print('Bot is Started!')
bot.run()
