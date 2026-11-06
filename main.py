import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from models import vk_bot
from commands import *
from secret_keys import TOKEN, PUBLIC_ID

def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, PUBLIC_ID)
    vk = vk_session.get_api()
    bot = vk_bot.Vk_bot()

    for event in longpoll.listen():
        if event.type != VkBotEventType.MESSAGE_NEW: # Скипаем все события, кроме сообщений
            continue
        if event.from_chat or not event.from_user:   # Скипаем все сообщения из чатов и от других сообществ
            continue

        # все действия далее - с сообщениями из лс
        message, keyboard = bot.process_msg(event.message.text, event.message.from_id)
        send_msg(vk, event.message.from_id, message, keyboard=keyboard)

if __name__ == "__main__":
    main()