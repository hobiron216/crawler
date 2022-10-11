from telethon import TelegramClient, events, sync
from datetime import date, timezone, datetime
from pprint import pprint
import json
import re
import logging
import traceback
import time
import sys
import hashlib
from elasticsearch import Elasticsearch, helpers
# import mysql.connector



# group_id = sys.argv[1]
# group_name = sys.argv[2]
# group_name = group_name.replace("#", " ")
# if group_id == "1697685344":
#     group_name = " Trading Octafx Malaysia "
# elif group_id == "1626304506":
#     group_name = "investment Global Trader MALAYSIA"
#
# mydb = mysql.connector.connect(
#     host="192.168.99.139",
#     user="root",
#     password="rahasia2016",
#     database="db_tele_secom",
#     autocommit = False
# )
#
# mycursor = mydb.cursor()
# sql_query = mycursor.execute('''Select * from recrawl where id='''+ group_id)
# data_mysql =mycursor.execute(sql_query)
# mydb.commit()
#
# for aw in data_mysql:
#     print(aw)
# sys.exit()

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

api_id = 2852480
api_hash = 'fb9e5153889b3ec9fb7f6edcb443fb42'
client = TelegramClient('session', api_id, api_hash)

# _index = "my_telegram_secom"
# es = Elasticsearch(
#     [{'host': '192.168.114.152', 'port': 9200}],
#     # _ip.split(", "),
#     # sniff before doing anything
#     sniff_on_start=True,
#     # refresh nodes after a node fails to respond
#     sniff_on_connection_fail=True,
#     # and also every 60 seconds
#     sniffer_timeout=100,
#     http_auth=('esph_my', '3Smy2o2!')
# )

# d = date(2020, 12, 14)

# async def get_all_file(message):
#     # You can download media from messages, too!
#     # The method will return the path where the file was saved.
#     if message.photo:
#         path = await message.download_media()
#         logging.info('File saved to', path)  # printed after download is done


# async def get_client_data(me):
#     # Getting information about yourself
#     me = await client.get_me()
#     # "me" is a user object. You can pretty-print
#     # any Telegram object with the "stringify" method:
#     logging.info(me.stringify())

#     # When you print something, you see a representation of it.
#     # You can access all attributes of Telegram objects with
#     # the dot operator. For example, to get the username:
#     username = me.username
#     logging.info(username)
#     logging.info(me.phone)


async def print_group_dialog():
    # You can print all the dialogs/conversations that you are part of:
    list = []
    async for dialog in client.iter_dialogs():
        # print(dialog)
        dialog_name = re.sub(r'[\\/*?:"<>|]', "_", dialog.name)
        dialog_name = re.sub('[^A-Za-z0-9]+', ' ', dialog_name)

        d = f"{dialog_name}#{dialog.id}"

        result = {
           "name" : dialog.name,
           "id" : dialog.id
       }
        list.append(result)
        # list.append(d) if dialog.id < 0 else ""
    return list


# async def sending_message():
#     # You can send messages to yourself...
#     await client.send_message('me', 'Hello, myself!')
#     # ...to some chat ID
#     await client.send_message(-3424, 'Hello, group!')
#     # ...to your contacts
#     await client.send_message('231', 'Hello, friend!')
#     # ...or even to any username
#     await client.send_message('exapmle', 'Testing Telethon!')

#     # You can, of course, use markdown in your messages:
#     message = await client.send_message(
#         'me',
#         'This message has **bold**, `code`, __italics__ and '
#         'a [nice website](https://example.com)!',
#         link_preview=False
#     )

#     # Sending a message returns the sent message object, which you can use
#     logging.info(message.raw_text)

#     # You can reply to messages directly if you have a message object
#     await message.reply('Cool!')

#     # Or send files, songs, documents, albums...
#     await client.send_file('me', '')

def bulk_insert(data, _index):

    while True:
        try:
            response = helpers.bulk(es, data, index=_index, doc_type="_doc", request_timeout=20)
            break
        except Exception as e:
            print("timeout")
            # print(e)
            # time.sleep(1)
            # sys.exit()
            continue
            logger.error(f"{self.bulk_insert.__name__} : {absolute_path}")

def utc_to_local(utc_dt):
    # return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return utc_dt


def get_date(dt):
    return dt.strftime("%Y%m%d %H:%M:%S")


def get_message_type(message):
    # type(message.media).__name__
    if message.photo:
        return "file - photo"
    elif message.document:
        return "file - document"
    elif message.text:
        return "text"
    else:
        return "None"


def get_message_fwd_detail(msg):
    # logging.info("O"*100)
    # logging.info(msg)
    # logging.info("O"*100)
    if msg is None:
        return "None", "None"
    else:
        try:
            fwd_id = str(msg.from_id.channel_id)
        except AttributeError as e:
            fwd_id = str(msg.from_id.user_id)
            # pass
        # r = f"{fwd_id} - {get_date(utc_to_local(msg.date))}"
        # logging.info(r)
        return fwd_id, get_date(utc_to_local(msg.date))


def get_message_reply(msg):
    if msg is None:
        return "None"

    else:
        return msg.reply_to_msg_id


def get_value(data):
    try:
        if data is None:
            return "None"
        elif not data:
            return "None"
        else:
            return str(data)
    except Exception as e:
        return "None"


def get_current_time(status):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d %H:%M:%S")
    lg = f"{status} : {dt_string}"
    logging.info(lg)
    print(lg)


async def get_all_data(dialogId, dialogName):
    # You can print the message history of any chat:
    json_data_list = []


    group_id = dialogId
    group_name = dialogName


    file_name = "/dataph/telegroup-crawl2/" + group_name + "_" + group_id + ".json"
    logging.info(file_name)
    # print(file_name)
    dialogId = int("-100" + dialogId)
    async for message in client.iter_messages(dialogId):
        try:
            json_data = await get_data(message, file_name, group_id,group_name)
            json_data_list.append(json_data)
        except Exception as e:
            traceback.print_exc()
            # pass
    logging.info(len(json_data_list))
    today = date.today()
    crawl_date = today.strftime("%Y%m%d")
    with open(file_name, 'w') as file:
        json.dump(json_data_list, file)


async def get_data(message, file_name, group_id, group_name  ):
    list_data = []
    try:

        sender = message.sender
        # print()
        # print(sender)
        # print(message)
        # print()

        message_date = utc_to_local(message.date)
        fwd_from_id, fwd_date = get_message_fwd_detail(message.fwd_from)
        reply_to_msg_id = get_message_reply(message.reply_to)
        first_name = get_value(sender.first_name)
        last_name = get_value(sender.last_name)
        if last_name:
            person = first_name + " " + last_name
        else:
            person = first_name
        id = file_name.replace("/dataph/telegroup-crawl2/telegram_secom/", "") + "_" + get_value(message.id)

        id = hashlib.md5(id.encode('utf-8')).hexdigest()
        date21 = get_date(message_date)
        year = date21[0:4]
        month = date21[4:6]
        date = date21[6:8]
        time = get_date(message_date).split(" ")[1]
        date_clean = year + "-" + month + "-" + date + "T" + time + ".000Z"
        json_data = {
            "_id" : id,
            "post_id": get_value(message.id),
            "person_id": get_value(sender.id),
            "person": person,
            "message": get_value(message.text),
            "type": get_message_type(message),
            "forward_from_id": fwd_from_id,
            "reply_to_msg_id": str(reply_to_msg_id),
            "date": str(date_clean),
            "time" : get_date(message_date).split(" ")[1],
            "time_epoch": datetime.timestamp(message_date),
            "group_name": str(group_name),
            "group_id": str(group_id)
            # "sender_username": get_value(sender.username),
            # "sender_first_name": get_value(sender.first_name),
            # "sender_last_name": get_value(sender.last_name),
            # "sender_phone": get_value(sender.phone),
            # "message_fwd_date": fwd_date,
            # "message_date": get_date(message_date),
        }
        # list_data.append(json_data)
        # bulk_insert(list_data, _index)

        return json_data
    except Exception as e:
        try:
            sender = message.sender
            message_date = utc_to_local(message.date)
            fwd_from_id, fwd_date = get_message_fwd_detail(message.fwd_from)
            reply_to_msg_id = get_message_reply(message.reply_to)
            id = file_name.replace("/dataph/telegroup-crawl2/", "") + "_" + get_value(message.id)

            id = hashlib.md5(id.encode('utf-8')).hexdigest()
            date21 = get_date(message_date)
            year = date21[0:4]
            month = date21[4:6]
            date = date21[6:8]
            time = get_date(message_date).split(" ")[1]
            date_clean = year + "-" + month + "-" + date + "T" + time + ".000Z"

            json_data = {
                "_id": id,
                "post_id": get_value(message.id),
                "person_id": get_value(sender.id),
                "person": get_value(sender.username),
                "message": get_value(message.text),
                "type": get_message_type(message),
                "forward_from_id": fwd_from_id,
                "reply_to_msg_id": str(reply_to_msg_id),
                "date": str(date_clean),
                "time" : get_date(message_date).split(" ")[1],
                "time_epoch": datetime.timestamp(message_date),
                "group_name": str(group_name),
                "group_id": str(group_id)
            }
            # list_data.append(json_data)
            # bulk_insert(list_data, _index)
            return json_data
        except Exception as e:
            pass


# async def test_message(dialogId, dialogName):
#     async for message in client.iter_messages(dialogId, 10):
#         print("*"*50)
#         print(type(message.sender))
#         print(message.sender)
#         print(message)
#         print("*"*50)
#         print()
#         # if (message.sender).channel:
#         #     print("yes")
#         # else:
#         #     print("no")

async def run(dialog):
    arr_dialog = dialog.split("#")
    dialog_id = arr_dialog[1]
    dialog_name = arr_dialog[0].strip()
    get_current_time("start")
    try:
        # logging.info(dialog)
        print(f"Grup ID :{int(dialog_id)}")
        print(f"Grup Name :{dialog_name}")
        await get_all_data(dialog_id, dialog_name)
    except Exception as e:
        print(e)
        print("wzzzzzzzzzzzzz")
        traceback.print_exc
    get_current_time("end")
    print()
    time.sleep(10)


async def main():
    # logging.basicConfig(filename='logs/logger.log', level=logging.INFO)
    # list = await print_group_dialog()
    # with open("/home/tele.json", 'w', encoding='utf8') as outfile:
    #     json.dump(list,outfile, ensure_ascii=False)
    # sys.exit()

    # sisa
    # list = [
    #         'Group Belajar Forex Malaysia#-1001358972412',
    #         'FOREX MALAYSIA FREE CHANNEL#-1001435782664',
    #         'Crypto Advisor Malaysia#-1001297200906',
    #         'AtikahFx academy Forex Education #-1001132869658',
    #         'MASTERMIND FX ASIA MMFX #-1001478874542',
    #         'ForexMart #-1001129431787',
    #         'Forex For Dummies #-1001220522118',
    #         'BTC Malaysia 2#-1001063984294'
    #         'Malaysia Crypto Community#-1001128651729',
    #         'KERABAT 77 NETWORK #-1001485856581',
    #         'EAcaptain ROBOT FOREX MALAYSIA#-1001390868676',
    #         'MT 4 FX #-1001261887450',
    #         'PROFIT USD#-1001325196422',
    #  'FOREX GENIUS #-1001309814069',

    #         'Forsage Malaysia Real Ethereum Platform #-1001290121914'
    #         ]

    # get_current_time("start")

    group_id = "1513472207"
    group_name = "china2"
    await get_all_data(group_id, group_name)
    # # await test_message(-1001128651729, "Malaysia Crypto Community")
    # get_current_time("end")

    # logging.info(list)
    # pprint(list)
    # pprint(len(list))
    # list = ["OCTA FX INVEST#-1001782248000"]
    # for i in list:
    #     await run(i)



with client:
    client.loop.run_until_complete(main())
