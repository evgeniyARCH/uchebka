import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from models import vk_bot
from commands import *

AE_TOKEN = "ab70ca0707d94699fe22b0145df14e061b834b9671e0ec2f426919db9863fb006fc78f9e05f2f38aea67b"
AE_PUBLIC_ID = '213488833'

vk_session = vk_api.VkApi(token=AE_TOKEN)
longpoll = VkBotLongPoll(vk_session, AE_PUBLIC_ID)
vk = vk_session.get_api()

def main():
    active = {}

    for event in longpoll.listen():
        if event.type != VkBotEventType.MESSAGE_NEW: # Обработка только сообщений
            continue
        if event.from_chat or not event.from_user:   # Обработка только лс
            continue

        request = event.message.text
        # scan_days = sd.scan_days()
        # count_user = format.count_for_userid(event.user_id, scan_days)
        # print(count_user)
        # user = vk.method("users.get", {"user_ids": event.user_id})
        # user_name = user[0]['first_name']
        bot = vk_bot.Vk_bot(request, event.message.from_id, active)
        message, keyboard, active = bot.otvet()
        send_msg(vk, event.message.from_id, message, keyboard=keyboard)

if __name__ == "__main__":
    main()