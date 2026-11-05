import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from models import vk_bot

def write_msg(user_id, message, keyboard):
    vk.method('messages.send',
              {'user_id': user_id, 'message': message, 'random_id': get_random_id(), 'keyboard': keyboard})

def send_msg(peer_id, text, keyboard='', attachment=''):
    vk.messages.send(peer_id=peer_id, message=text, random_id=get_random_id(),
                     keyboard=keyboard, attachment=attachment)

AE_token = "ab70ca0707d94699fe22b0145df14e061b834b9671e0ec2f426919db9863fb006fc78f9e05f2f38aea67b"
vk = vk_api.VkApi(token=AE_token)
longpoll = VkBotLongPoll(vk)

active = {}

for event in longpoll.listen():
    if event.type != VkBotEventType.MESSAGE_NEW: # Обработка только сообщений
        continue
    if event.from_chat or not event.from_user:   # Обработка только лс
        continue

    request = event.text
    # scan_days = sd.scan_days()
    # count_user = format.count_for_userid(event.user_id, scan_days)
    # print(count_user)
    # user = vk.method("users.get", {"user_ids": event.user_id})
    # user_name = user[0]['first_name']
    bot = vk_bot.Vk_bot(request, event.user_id, active)
    message, keyboard, active = bot.otvet()
    write_msg(event.user_id, message, keyboard)