import datetime
import re
import time
from geopy.geocoders import Nominatim
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions, ChatMemberUpdated, ChatActions
from aiogram.utils import executor
import random
from glob import glob
import os, shutil
from telethon.sync import TelegramClient
import asyncio
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.filters import Text
from config import api_id, api_hash, phone_number, API_TOKEN

API_TOKEN = '5697477278:AAF5WZh1X-6u9MzcHp0ic4tnIX__2_xtHtU'
api_id = 27703999
api_hash = 'ef67c9e77303b6d0902d2df5b75afda4'
phone_number = '+375295835409'

# Создайте экземпляр бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

with open('words.txt', 'r', encoding='utf-8') as file:
    bad_words = [word.strip().lower() for word in file if word.strip()]

pattern = '|'.join(bad_words)
# Создайте регулярное выражение для поиска матерных слов
bad_words_pattern = re.compile(pattern, re.IGNORECASE)

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

@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    await anti_flood(message)
    await message.answer('здарова петушары!')
    await message.delete()
    ids = await get_chat_user_ids(api_id, api_hash, phone_number, message.chat.id)
    print(ids)

@dp.message_handler(commands=['mute', 'unmute'])
async def mute_command_handler(message: types.Message):
     await anti_flood(message)
     isadmin = await bot.get_chat_member(message.chat.id, message.from_user.id)
     if isadmin.is_chat_admin():
         if not message.reply_to_message:
             await message.delete()
             await bot.send_message(message.from_user.id,'команда должна быть ответом на сообщение')
             return
         user_id = message.reply_to_message.from_user.id

         if message.text == '/unmute':
             permissions = ChatPermissions(can_send_messages=True)
             await bot.restrict_chat_member(message.chat.id, user_id, permissions, until_date=100000)
             await message.delete()
             return
         else:
             mute_sec = int(message.text[6:])
             mute_time = datetime.datetime.now() + datetime.timedelta(seconds=mute_sec)
             permissions = ChatPermissions(can_send_messages=False)
             await bot.restrict_chat_member(message.chat.id, user_id, permissions, until_date=mute_time)
             await message.delete()

@dp.message_handler(commands=['joke'])
async def joke_command_handler(message: types.Message):
    await anti_flood(message)
    await bot.send_message(message.from_user.id,"Хоть я и несуществовал, но мать твою в очко ебал")
    await message.delete()



@dp.message_handler(commands=['summer'])
async def summer_command_handler(message: types.Message):
    await anti_flood(message)
    today = datetime.date.today().year
    target_date = datetime.date(today, 6, 1)
    if datetime.date.today().month > 5 and datetime.date.today().month < 9:
        today = datetime.date.today().year
        target_date = datetime.date(today, 9, 1)
        current_date = datetime.date.today()
        time_diff = target_date - current_date
        await  bot.send_message(message.from_user.id,f"дней до лета: {time_diff.days} дней")
    else:
        current_date = datetime.date.today()

        # вычисляем разницу между датами
        time_diff = target_date - current_date
        await bot.send_message(message.from_user.id,f"дней до лета: {time_diff.days} дней")
    await message.delete()

@dp.message_handler(commands=['weather'])
async def weather_command_handler(message: types.Message):
    await anti_flood(message)
    api = 'ff7241f24f05023868c977c325973182'
    geolocator = Nominatim(user_agent="my-custom-agent")  # Создание объекта геокодера
    location = geolocator.geocode("Zhabinka")  # Получение объекта местоположения по названию города
    lat = location.latitude
    lon = location.longitude # Вывод координат местоположенияp
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}&units=metric&lang=ru')
    data = r.json()
    city = data['name']
    weather = data['weather'][0]['description']
    wind = data['wind']['speed']
    temperature = data['main']['temp']
    temperature_feels = data['main']['feels_like']
    clouds = data['clouds']['all']
    await bot.send_message(message.from_user.id,f"погода в городе <b>{city}</b>: \n"
                         f"{weather}\n"
                         f"температура: <b>{temperature}</b>, ощущается как <b>{temperature_feels}</b>, \n"
                         f"облачность:<b>{clouds} </b>%\n"
                         f"ветер: <b>{wind} м/с</b>", parse_mode='html')
    await message.delete()

@dp.message_handler(commands=['image'])
async def image_command_handler(message:types.Message):
    await anti_flood(message)
    block_time = 0
    # if block_time >= datetime.datetime.today().:
    chat = message.chat.id
    all_files = []
    path = "c:/Users/bokho/Downloads/Мессенджер"
    os.chdir(path)
    listdir = glob('*')
    if not listdir:
        await message.answer('кончились фотки, вы ебаные уёбки!))')
        return
    rand_img = random.choices(listdir, k=3)

        # создаем список InputMedia для каждой из трех случайно выбранных фотографий
    media_list = []
    for img_name in rand_img:
        photo_path = f"{path}/{img_name}"
        with open(photo_path, 'rb') as f:
            photo = f.read()
            await bot.send_photo(message.chat.id,photo)
    # block_time = datetime.datetime.now() + datetime.time.hour(3)

@dp.message_handler(commands=['help'])
async def help_command_handler(message:types.Message):
    await anti_flood(message)
    await bot.send_message(message.from_user.id,'этот бот следит за ссаниной происходящей в этом легендарном чате')
    await message.delete()

@dp.message_handler(commands=['currency'])
async def currency_command_handler(message:types.Message):
    await anti_flood(message)
    r = requests.get('https://belarusbank.by/api/kursExchange?city=Жабинка')
    data = r.json()
    usd_in = data[0]['USD_in']
    usd_out = data[0]['USD_out']
    eur_in = data[0]['EUR_in']
    eur_out = data[0]['EUR_out']
    rub_in = data[0]['RUB_in']
    rub_out = data[0]['RUB_out']
    pln_in = data[0]['PLN_in']
    pln_out = data[0]['PLN_out']
    # uah_in = data['UAH_in']
    # uah_out = data['UAH_out']
    await bot.send_message(message.from_user.id,f"курсы валют на сегодня:\n"
                   f"Доллар:\n"
                      f"     покупка: <b>{usd_in}</b>\n"
                      f"     продажа: <b>{usd_out}\n</b>\n"
                   f"Евро:\n"
                      f"     покупка: <b>{eur_in}</b>\n"
                      f"     продажа: <b>{eur_out}\n</b>\n"
                   f"Российский рубль:\n"
                      f"     покупка: <b>{rub_in}</b>\n"
                      f"     продажа: <b>{rub_out}\n</b>\n"
                   f"Польский злотый:\n"
                      f"     покупка: <b>{pln_in}</b>\n"
                      f"     продажа: <b>{pln_out}\n</b>\n", parse_mode='html')
    #

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS,types.ContentType.LEFT_CHAT_MEMBER])
async def delete_join_messages(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message_handler()
async def filter_messages(message: types.Message):
    # Проверьте, содержит ли сообщение матерные слова
    await anti_flood(message)
    text = message.text.islower()
    # Проверяем, что пользователь не отправлял сообщение в последнюю минуту

    if bad_words_pattern.search(message.text.replace(' ', '')):
        # Ограничьте пользователя в отправке сообщений на 10 секунд
        chat_id = message.chat.id
        user_id = message.from_user.id

        await message.answer('я смотрю ты распизделся')
        await message.delete()
        mute_time = datetime.datetime.now() + datetime.timedelta(seconds = 60)
        permissions = ChatPermissions(can_send_messages=False)
        await bot.restrict_chat_member(chat_id, user_id, permissions, until_date=mute_time)










# Запустите бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
