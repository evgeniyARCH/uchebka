import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from random import randint

from datetime import datetime
from time import sleep

from models import vk_bot
from models import scan_days as sd
import time

def write_msg(user_id, message, keyboard):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id(), 'keyboard': keyboard})

# API-ключ созданный ранее
token = "vk1.a._nf9C7t0KwBh6HzJM3gQkN4lgNf_qPya2oUqvbULK9E4qHYWXXrTF7kcX6AdFUXiCTdfbK3chprQLYXRgHcdLaH0Uc2uKMA8kv1pNirw3vg_Az0MLDHFX5eVD_J-eXYIMh5Ec2hxn3bGePkHomo24aug-i8xjTJIFTWImFYqD1V61ynHiv54c9qwGmkp_pUfwQTpBzbS1rfnugigjrzzRw"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

active = {}

# Основной цикл
while True:
    try:
        for event in longpoll.listen():

            # Если пришло новое сообщение
            if event.type == VkEventType.MESSAGE_NEW:
            
                # Если оно имеет метку для меня( то есть бота)
                if event.to_me:
                
                    # Сообщение от пользователя
                    request = event.text
                    scan_days = sd.scan_days()
                    bot = vk_bot.Vk_bot(request, event.user_id, active, scan_days)
                    message, keyboard, active = bot.otvet()
                    write_msg(event.user_id, message, keyboard)
    except:
        print("Таймаут, переподключение...")
        # vk_keyboard = VkKeyboard()
        # keyboard = vk_keyboard.get_empty_keyboard()
        # message = 'Произошла ошибка. Попробуйте другую команду'
        # write_msg(event.user_id, message, keyboard)
        time.sleep(10)  # Ждем минуту перед повторной попыткой
    


# a = vk_bot.Vk_bot('Записаться на стирку', 333)
# a.otvet()

