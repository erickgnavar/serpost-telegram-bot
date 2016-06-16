#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

from telegram.ext import Updater, CommandHandler
import serpost


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')

format_result = lambda x: '{:%d-%m-%Y %H:%M}: {}'.format(x['date'], x['message'])


welcome_message = """
Welcome {user}
Use /track <tracking_number> to get information about your tracking number
"""


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text=welcome_message.format(user=update.message.from_user.first_name))


def track(bot, update, args):
    if len(args) and len(args[0]):
        code = args[0]
        result = serpost.query_tracking_code(code)
        if result:
            message = '\n'.join(map(format_result, result))
        else:
            message = 'No data'
    else:
        message = 'Please enter a tracking code'
    bot.sendMessage(update.message.chat_id, message)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(TELEGRAM_API_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('track', track, pass_args=True))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
