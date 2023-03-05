from aiogram import types, Bot, Dispatcher, executor
from other_functions import *
from config import *
import requests
import os, shutil
from glob import glob
from geopy.geocoders import Nominatim
import random
import re
from aiogram.types import BotCommand
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


with open('words.txt', 'r', encoding='utf-8') as file:
    bad_words = [word.strip().lower() for word in file if word.strip()]

pattern = '|'.join(bad_words)
# Создайте регулярное выражение для поиска матерных слов
bad_words_pattern = re.compile(pattern, re.IGNORECASE)



async def start_command_handler(message: types.Message):
    await anti_flood(message)
    await message.answer('здарова петушары!')
    await message.delete()
    ids = await get_chat_user_ids(api_id, api_hash, phone_number, message.chat.id)
    print(ids)


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
     else:
        await message.delete()
        await message.answer("нет прав доступа")

async def joke_command_handler(message: types.Message):
    await anti_flood(message)
    await bot.send_message(message.from_user.id,"Хоть я и несуществовал, но мать твою в очко ебал")
    await message.delete()




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


async def image_command_handler(message:types.Message):
    users_ids = []
    user_id = message.from_user.id
    if datetime.time(hour= 00, minute= 00, second= 00):
        users_ids.clear()
    if user_id in user_ids:
        message.delete()
        return
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
        os.remove(photo_path)

    users_ids.append(user_id)

async def help_command_handler(message:types.Message):
    await anti_flood(message)
    await bot.send_message(message.from_user.id,'этот бот следит за ссаниной происходящей в этом легендарном чате')
    await message.delete()


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


async def delete_join_messages(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



async def filter_messages(message: types.Message):
    chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if chat_member.is_chat_owner():
        return
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


