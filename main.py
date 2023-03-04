from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from config import api_id, api_hash, phone_number, API_TOKEN
from commands import *
from other_functions import *

# Создайте экземпляр бота




dp.register_message_handler(start_command_handler, commands=['start'])
dp.register_message_handler(help_command_handler, commands=['mute', 'unmute'])
dp.register_message_handler(joke_command_handler, commands=['joke'])
dp.register_message_handler(summer_command_handler, commands=['summer'])
dp.register_message_handler(weather_command_handler, commands=['weather'])
dp.register_message_handler(image_command_handler, commands=['image'])
dp.register_message_handler(help_command_handler, commands=['help'])
dp.register_message_handler(currency_command_handler, commands=['currency'])
dp.register_message_handler(delete_join_messages, content_types=[types.ContentType.NEW_CHAT_MEMBERS,types.ContentType.LEFT_CHAT_MEMBER])
dp.register_message_handler(filter_messages)












# Запустите бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
