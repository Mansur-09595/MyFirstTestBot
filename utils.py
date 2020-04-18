import requests
from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_keyboard():
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Прислать собачку'],['Заполнить анкету'],
        [contact_button, location_button]], resize_keyboard=True)
    return my_keyboard