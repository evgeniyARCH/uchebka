def get_command_data(event, button=''):
    # Данные формируются так: (команда, id автора, роль автора, id сообщения, id цели, роль цели, *остальное)
    # start нужна, если бота только добавили, чтобы /sync запустилась от имени любого пользователя
    data = {"command": "", "author_id": 0, "author_role": "", "text": event.message.text,
            "mess_id": 0, "aim_id": 0,git  "aim_role": "",
            "chat_id": 0, "vargs": [], "err_mess": "", "answer_text": ""}

    words = event.message.text.split(' ')  # Деление строки по аргументам
    command = words[0][1:] if len(words[0]) == 0 or words[0][0] == '/' else None  # Выбор команды из строки
    author_id, chat_id = event.message['from_id'], event.message['peer_id']  # Автор и чат достаются из события
    mess_id = event.message['conversation_message_id']  # как и id сообщения

    if not command:
        vargs = words
    data["vargs"] = vargs

    data["command"], data["author_id"], data["author_role"] = command, author_id, author_role
    data["mess_id"], data["aim_id"] = mess_id, aim_id
    data["aim_role"], data["chat_id"] = aim_role, chat_id

    print(command, author_id, author_role, mess_id, aim_id, aim_role, chat_id, vargs)
    return data