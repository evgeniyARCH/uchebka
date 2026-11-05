TOKEN = 'ab70ca0707d94699fe22b0145df14e061b834b9671e0ec2f426919db9863fb006fc78f9e05f2f38aea67b'
PUBLIC_ID = '213488833'

#AE_token = "ab70ca0707d94699fe22b0145df14e061b834b9671e0ec2f426919db9863fb006fc78f9e05f2f38aea67b"


import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, PUBLIC_ID)

    for event in longpoll.listen():
        if event.type == VkBotEventType.BOARD_POST_NEW:
            print(event.obj['text'])
        print(event)



if __name__ == '__main__':
    main()
