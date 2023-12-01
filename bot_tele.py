import requests
import telebot
import datetime
from config import api_token,bot_api

bot = telebot.TeleBot(bot_api)

@bot.message_handler(commands=['start'])
def start(message): 
    bot.send_message(message.chat.id, 'Привет, я подскажу тебе погоду. Введи пожалуйста название города')

@bot.message_handler()
def weather_message(message):
    bot.send_message(message.chat.id,weather(message.text,api_token))

def weather(town,token):
    smiles_dict = {
        'Clear':'Ясно \U00002600',
        'Clouds':'Облачно \U00002601',
        'Rain':'Дождь \U00002614',
        'Drizzle':'Дождь \U00002614',
        'Thunderstorm':'Гроза \U000026A1',
        'Snow':'Снег \U0001F328',
        'Mist':'Туман \U0001F328'
    }

    try:
        req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={town}&appid={token}&units=metric')
        result = req.json()

        weather = result['main']['temp']
        weather_desc = result['weather'][0]['main']
        if weather_desc in smiles_dict:
            weather_desc = smiles_dict[weather_desc] 
        else:
            'Погода не определена'
        humidity = result['main']['humidity']
        pressure = result['main']['pressure']
        wind_speed = result['wind']['speed']
        sunrise_time = datetime.datetime.fromtimestamp(result['sys']['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(result['sys']['sunset'])
        length_of_the_day = sunset_time-sunrise_time
        return f'***{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}***\nПогода в городе {town}\nТемпература - {weather} C° {weather_desc}\nВлажность - {humidity} %\nДавление - {pressure} мм.рт.ст.\nСкорость ветра - {wind_speed} м/c\nВремя рассвета - {sunrise_time}\nВремя заката - {sunset_time}\nПродолжительность светового дня - {length_of_the_day}'
    except Exception:
        return 'Проверьте название города'


bot.infinity_polling()