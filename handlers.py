from random import choice

from telegram import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram.ext import messagequeue as mq

from utils import get_keyboard, get_url

subscribers = set()

def start(bot, update, user_data):
    msg = f'Hello {update.message.chat.first_name} !'
    update.message.reply_text(msg, reply_markup=get_keyboard())

 
#функция будет отвечать вам тем же сообщением
def text_msg(bot, update, user_data):
    msg = 'Ты написал {} !'.format(update.message.text)
    update.message.reply_text(msg)

@mq.queuedmessage
def send_dog_pic(bot,update, user_data):
    url = get_url()
    bot.send_photo(chat_id=update.message.chat.id, photo=url)

def subscribe(bot, update):
    if update.message.chat_id not in subscribers:
        subscribers.add(update.message.chat_id)
        update.message.reply_text("Вы подписались, наберите /unsubscribe чтобы отписаться")
    else:
        update.message.reply_text('Вы уже подписаны!')


def send_dog(bot, job):
    url = get_url()
    for chat_id in subscribers:
        bot.send_photo(chat_id=chat_id, photo=url)
        
def unsubscribe(bot, update):
    if update.message.chat_id in subscribers:
        subscribers.remove(update.message.chat_id)
        update.message.reply_text("Собачки вас больше не побеспокоят!")
    else:
        update.message.reply_text("Вы не подписаны, наберите/subscribe чтобы подписаться")


def alarm(bot, job):
    bot.send_message(chat_id=job.context, text="Сработал будильник!")

def set_alarm(bot, update, args, job_queue):
    try:
        seconds = abs(int(args[0]))
        job_queue.run_once(alarm, seconds, context=update.message.chat_id)
    except (IndexError, ValueError):
        update.message.reply_text("Введите число секунд после команды /alarm")


def anketa_start(bot, update, user_data):
    update.message.reply_text('Как вас зовут? Напишите имя и фамилию', reply_markup=ReplyKeyboardRemove())
    return 'name'

def anketa_get_name (bot, update, user_data):
    user_name = update.message.text
    if len(user_name.split( " ")) < 2:
        update.message.reply_text( "Пожалуйста, напишите имя и фамилию" )
        return "name"
    else:
        user_data[ "anketa_name"] = user_name
        reply_keyboard = [[ "1", "2", "3", "4", "5"]]
        update.message.reply_text(
            "Понравился ли вам курс? Оцените по шкале от 1 до 5" ,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard =True)
        )
        return "rating"

def anketa_rating(bot, update, user_data):
    user_data["anketa_rating"] = update.message.text
    update.message.reply_text("""Оставьте комментарий в свободной форме 
        или пропустите этот шаг, введя /skip""")
    return "comment"


def anketa_comment(bot, update, user_data):
    user_data["anketa_comment"] = update.message.text
    user_text = """
<b>Имя Фамилия:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}
<b>Комментарий:</b> {anketa_comment}""".format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(),
                                parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def anketa_skip_comment(bot, update, user_data):
    user_text = """
<b>Имя Фамилия:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}""".format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(),
                                parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def dont_know(bot, update, user_data):
    update.message.reply_text('Упс! Что-то не так !')
