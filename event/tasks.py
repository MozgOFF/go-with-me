from __future__ import absolute_import, unicode_literals
from time import sleep
from celery import shared_task
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, CreateChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from .models import Event

api_id = 1329156
api_hash = '8fd6064629c2fe25b79a20d84eda3196'


@shared_task
def create_telegram_chat(eid, desc):

    with TelegramClient('session_name', api_id, api_hash) as client:
        title = 'Gowithme-' + str(eid)
        group = client(CreateChannelRequest(title=title, about=desc, megagroup=True))
        print("asdasdasddas,", dir(group))
        for dialog in client.iter_dialogs():
            if dialog.title == title:
                result = client(ExportChatInviteRequest(dialog))
                link = result.link
                event = Event.objects.get(id=eid)
                event.telegram_chat = link
                event.save()
                return

