from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, RegexHandler, Updater
from telegram.ext import messagequeue as mq

from config import PROXY, TOKEN
from handlers import anketa_comment, anketa_rating, anketa_start, anketa_skip_comment, anketa_get_name, dont_know, start, send_dog, subscribe, send_dog_pic, set_alarm, text_msg, unsubscribe

from utils import get_keyboard, get_url

def main():
    bot = Updater(TOKEN, request_kwargs=PROXY) 
    dp = bot.dispatcher

    bot.bot._msg_queue = mq.MessageQueue()
    bot.bot._is_messages_queued_default = True

    anketa = ConversationHandler(
                entry_points=[RegexHandler('^(Заполнить анкету)$', anketa_start, pass_user_data=True)],
                states={"name": [MessageHandler(Filters.text, anketa_get_name, pass_user_data=True)],
                        "rating": [RegexHandler('^(1|2|3|4|5)$', anketa_rating, pass_user_data=True)],
                        "comment": [MessageHandler(Filters.text, anketa_comment, pass_user_data=True),
                                    CommandHandler('skip', anketa_skip_comment, pass_user_data=True)]},
                fallbacks=[MessageHandler(Filters.text, dont_know, pass_user_data=True)]
                            )
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('start', start, pass_user_data=True))
    dp.add_handler(CommandHandler('dog', send_dog_pic, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать собачку)$', send_dog_pic, pass_user_data=True))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CommandHandler("alarm", set_alarm, pass_args=True, pass_job_queue=True))
    dp.add_handler(MessageHandler(Filters.text, text_msg, pass_user_data=True))
    
    bot.start_polling()
    bot.idle()

if __name__ == "__main__":
    main()