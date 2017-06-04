from telegram.ext import Updater
from telegram.ext import CommandHandler,MessageHandler,Filters,ConversationHandler
import logging
import os
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
INPUT, STORE, OUT = range(3)


def start(bot_instance, update):
    bot_instance.send_message(chat_id=update.message.chat_id, text='Talk dirty to me bitch')
    return INPUT


def req_value(bot_instance, update,user_data):
    bot_instance.send_message(chat_id=update.message.chat_id, text='Now send an input')
    print(user_data)
    return STORE


def done(bot_instance, update):
    bot_instance.send_message(chat_id=update.message.chat_id, text='done')
    return ConversationHandler.END


def store_value(bot_instance, update,user_data):
    user_data['input']=update.message.text
    bot_instance.send_message(chat_id=update.message.chat_id, text='your input has been stored! :)')
    print(user_data)
    return OUT


def output_value(bot_instance, update,user_data):
    bot_instance.send_message(chat_id=update.message.chat_id, text=user_data['input'])


def unknown(bot_instance, update):
    bot_instance.send_message(chat_id=update.message.chat_id, text='Sorry! no such command :(')


# bot = telegram.Bot(token='387093650:AAGb4uZjtt71N4LVPn_flI8JKTOWFy_ZW10')
# updater = Updater(token='387093650:AAGb4uZjtt71N4LVPn_flI8JKTOWFy_ZW10')
# dispatcher = updater.dispatcher

'''adding handlers'''
#
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
#
# input_handler = CommandHandler('input', req_value, pass_user_data=True)
# dispatcher.add_handler(input_handler)
#
# input_store_handler = MessageHandler(Filters.text, store_value, pass_user_data=True)
# dispatcher.add_handler(input_store_handler)
#
# output_handler = CommandHandler('output', output_value, pass_user_data=True)
# dispatcher.add_handler(output_handler)
#
# unknown_handler = MessageHandler(Filters.command, unknown)
# dispatcher.add_handler(unknown_handler)

'''firing up the bot'''


def main():
    
    TOKEN = "387093650:AAGb4uZjtt71N4LVPn_flI8JKTOWFy_ZW10"
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
               INPUT: [CommandHandler('input', req_value, pass_user_data=True)],
               STORE: [MessageHandler(Filters.text,store_value,pass_user_data=True)],
               OUT: [CommandHandler('output',output_value,pass_user_data=True)],
        },
        fallbacks=[CommandHandler('done', done)]
    )
    
    dp.add_handler(conv_handler)
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://test-levi-bot.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()
