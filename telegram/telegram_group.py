from telethon import TelegramClient, sync
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import json
import datetime
from dateutil import tz
from datetime import date
from pathlib import Path
import sys


# login session akun dgn nomor hp (083890436921) dan dikirm kode
class Crawling_Telegram :
    def __init__(self):
        self.api_id = 2369334
        self.api_hash = "f244a6b931ae521660275cb42ce1ed18"

        self.to_zone = tz.tzlocal()

    def crawl_date(self):
        today = date.today()
        crawl_date = today.strftime("%Y%m%d")
        return  crawl_date

    def create_folder(self, crawl_date):
        Path("/dataph/telegroup-crawl2/" + crawl_date + "/").mkdir(parents=True,exist_ok=True)

    def get_group(self, session):
        self.client = TelegramClient('session_name'+ session, self.api_id, self.api_hash).start()
        last_date = None
        chunk_size = 200
        chats = []
        groups = []
        result = self.client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        chats.extend(result.chats)
        for chat in chats:
            try:
                # if chat.megagroup == True:
                #     groups.append(chat)
                groups.append(chat)
            except:
                continue

        return groups

    def parse_group(self,name_group,session):
        i = 0
        b = 0
        groups=self.get_group(session)
        for g in groups:
            try :
                group = g.title
                group = group.encode('ascii', 'ignore').decode('ascii')
                if "Edisi" in group:
                    print(group)
                a = g.title
                if b == a:
                    continue
                b = a
                # print(group)
                # continue
                # print(i)
                # continue
                if group == name_group:
                    print("wwkwkwk")
                    i=i+1
                    # print(g.broadcast)
                    # continue
                    # print(group)
                    # print(i)
                    # continue

                    print("GROUP :" + group)
                    database_nama = []

                    try :
                        participants = self.client.get_participants(g.title)
                        if len(participants):
                            i=0
                            for x in participants:
                                i=i+1
                                data_nama={
                                    "id" : x.id,
                                    "first_name" : x.first_name,
                                    "last_name": x.last_name,
                                    "username": x.username

                                }
                                database_nama.append(data_nama)
                    except:
                        person="Admin"



                    chats = self.client.get_messages(g.title, limit=None) # n number of messages to be extracted
                    datas=[]
                    if len(chats):

                        i=0
                        for chat in chats:
                            try :
                                i=i+1

                                for y in database_nama:
                                    try :
                                        if y['id']==chat.from_id.user_id:

                                            if y['last_name'] == None:
                                                person=y['first_name']
                                                break
                                            else :
                                                person= y['first_name'] + " " + y['last_name']
                                                break
                                    except:
                                        person="Admin"

                                message=chat.message
                                if not message:
                                    message="None"

                                if chat.action:
                                    if "Pin" in str(chat.action):
                                        type = "pin message"
                                    elif "Delete" in str(chat.action):
                                        type = "delete user"
                                    else :
                                        type="join grup"
                                else :
                                    if chat.media:
                                        try :
                                            r=chat.media.document.attributes
                                            for item in r:
                                                type="file - " + item.file_name
                                        except:
                                            try :
                                                r=chat.media.photo
                                                type= "file - photo"
                                            except:
                                                if "Poll" in str(chat.media):
                                                    type="poll"
                                                else:
                                                    type = "text"

                                    else :
                                        type = "text"

                                time21=chat.date
                                time21=time21.astimezone(self.to_zone)
                                time21=str(time21)
                                time21=(time21.split(" "))

                                date = datetime.datetime.strptime(time21[0],"%Y-%m-%d")
                                date = date.strftime("%Y%m%d")
                                time = time21[1].split("+")
                                time = datetime.datetime.strptime(time[0], "%H:%M:%S")
                                time= time.strftime("%H:%M:%S")

                                time_epoch=int(chat.date.timestamp())
                                reply=chat.reply_to_msg_id
                                try:
                                    person_id = str(chat.from_id.user_id)
                                except:
                                    person_id="None"
                                try :
                                    forward=chat.fwd_from
                                    if forward == None:
                                        forward = "None"
                                    else :
                                        forward = chat.fwd_from.from_id.user_id
                                except:
                                    pass

                                if message ==None:
                                    message="None"
                                if reply == None:
                                    reply="None"

                                if g.broadcast==True:
                                    person="Admin"
                                    person_id="None"
                                    forward = chat.fwd_from
                                    if forward == None:
                                        forward = "None"
                                    else:
                                        try :
                                            forward = chat.fwd_from.from_id.user_id
                                        except:
                                            forward= str(g.id)

                                data ={
                                       'post_id' : str(chat.id),
                                       'person_id' : person_id,
                                       'person' :person,
                                       'message': message,
                                        'type': type,
                                        'forward_from_id' : str(forward),
                                        'reply_to_msg_id': reply,
                                        'date' : date,
                                       'time':time,
                                        'time_epoch' : str(time_epoch)
                                }

                                datas.append(data)
                                # print(str(chat).encode('utf-8'))
                            except Exception as e:
                                print(e)
                                continue

                        datas21=json.dumps(datas)

                        crawl_date = self.crawl_date()
                        self.create_folder(crawl_date)
                        with open("/dataph/telegroup-crawl2/"+ crawl_date + "/" + group + "_" + str(g.id) + ".json",'w', errors='ignore') as outfile:
                            outfile.write(datas21)
                        del datas[:]
                        del database_nama[:]
            except ValueError or AttributeError or UnboundLocalError:
                raise
        print("success")

# name_group =sys.argv[1]
# session = sys.argv[2]

name_group = "Edisi Siasat"
session = "b"
if name_group!=None and session!=None:
    Crawling_Telegram().parse_group(name_group, session)
else :
    print("Nama Grup atau Session Salah")
