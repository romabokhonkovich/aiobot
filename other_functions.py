users_dict = {}

async def anti_flood(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = datetime.datetime.now()

    if user_id not in users_dict:
        # Создаем запись в словаре для пользователя
        users_dict[user_id] = {"message_count": 1, "last_message_time": current_time}
    else:
        last_message_time = users_dict[user_id]["last_message_time"]
        delta = current_time - last_message_time

        if delta < datetime.timedelta(seconds=10):
            users_dict[user_id]["message_count"] += 1
        else:
            users_dict[user_id] = {"message_count": 1, "last_message_time": current_time}

    if users_dict[user_id]["message_count"] > 3:
        # Ограничиваем права отправки сообщений пользователю на 60 секунд
        permissions = ChatPermissions(can_send_messages=False)
        until_date = datetime.datetime.now() + datetime.timedelta(seconds=60)
        await message.chat.restrict(user_id, permissions, until_date=until_date)
        await message.reply("овцеёб блохастый, угомонись")


async def get_chat_user_ids(api_id, api_hash, phone_number, chat_id):
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        # Получить объект чата по имени
        # Получить список участников чата
        participants = await client.get_participants(chat_id, aggressive=True)

        # Извлекаем только идентификаторы пользователей
        user_ids = {f"{user.first_name}":user.id for user in participants if not user.bot}

    return user_ids
