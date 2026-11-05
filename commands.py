admin_ids = (234583753, )

''' Данные о сообщении формируются так:
(команда, id автора, роль автора, текст сообщения, id сообщения, id цели, роль цели,
сообщение ошибки при ошибке, текст ответа, *остальное)
'''

def get_command_data(event, button=''):
    data = {"command": "", "author_id": 0, "author_role": "", "text": event.message.text,
            "mess_id": 0, "aim_id": 0, "aim_role": "",
            "err_mess": "", "answer_text": "", "vargs": []}

    words = event.message.text.split(' ')  # Деление строки по словам
    command = words[0][1:] if words[0][0] == '/' else None  # Выбор команды из строки
    author_id, chat_id = event.message['from_id'], event.message['peer_id']  # Автор и чат достаются из события
    mess_id = event.message['conversation_message_id']  # как и id сообщения

    author_role = author_id in admin_ids   # если айди чела в списке админов, то он админ (логично

    if not command:
        vargs = words
        aim_id, aim_role = author_id, author_role
    else:
        # Проверка указания цели через упоминание с помощью "@", тогда в тексте будет [id234583753|@hylkoid]
        if len(words) > 1 and '|' in words[1] and words[1][0] == '[' and words[1][-1] == ']':
            aim = words[1].replace('id', '')
            aim_id = int( aim[ 1:aim.find('|') ] )
            aim_role = aim_id in admin_ids
            vargs = words[2:]
        else:
            aim_id, aim_role = author_id, author_role
            vargs = words[1:]

    data["vargs"] = vargs
    data["command"], data["author_id"], data["author_role"] = command, author_id, author_role
    data["mess_id"], data["aim_id"] = mess_id, aim_id
    data["aim_role"], data["chat_id"] = aim_role, chat_id

    print(command, author_id, author_role, mess_id, aim_id, aim_role, chat_id, vargs)
    return data