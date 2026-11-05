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

        bot = vk_bot.Vk_bot(event.message.text, event.message.from_id, active)
        message, keyboard, active = bot.otvet()
        send_msg(vk, event.message.from_id, message, keyboard=keyboard)

if __name__ == "__main__":
    main()