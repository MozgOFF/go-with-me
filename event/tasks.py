from __future__ import absolute_import, unicode_literals
from time import sleep
from celery import shared_task
from telethon import TelegramClient, sync
from telethon.tl.functions.channels import InviteToChannelRequest, CreateChannelRequest


@shared_task
def h():
    print("<<>><<<<<<<<<<<<<-------------------------------------------------")


@shared_task
def create_telegram_chat(title):
    api_id = 1329156
    api_hash = '8fd6064629c2fe25b79a20d84eda3196'

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    group = client(CreateChannelRequest(title=title, about=title, megagroup=True))


@shared_task
def invite_to_telegram_chat(title, username):
    api_id = 1329156
    api_hash = '8fd6064629c2fe25b79a20d84eda3196'

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    user = client.get_entity('@{}'.format(username))
    for dialog in client.iter_dialogs():
        if dialog.title == title:
            client(InviteToChannelRequest(dialog, [user]))
    client.disconnect()
    # group = client(CreateChannelRequest(title=title, about=title, megagroup=True))
