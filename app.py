#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os

import serpost
from telegram.ext import CommandHandler, Updater


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('serpost.telegram.bot')

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')


def format_result(record):
    return '{:%d-%m-%Y %H:%M}: {}'.format(record['date'], record['message'])


help_message = """
/track - track a package with the tracking number
"""

welcome_message = """
Welcome {user}
You can control me by sending these commands:
""" + help_message


def start_handler(bot, update):
    bot.sendMessage(update.message.chat_id, text=welcome_message.format(user=update.message.from_user.first_name))
    logger.info('New user: %s', update.message.from_user.first_name)


def track_handler(bot, update, args):
    if len(args) == 2 and args[0] and args[1]:
        code = args[0]
        year = args[1]
        logger.info('Tracking code: %s and year: %s', code, year)
        result = serpost.query_tracking_code(code, year=year)
        if result:
            message = '\n'.join(map(format_result, result))
        else:
            message = 'No data'
    else:
        message = 'Please enter a tracking code and a valid year, eg /tracking ABC123 2018'
    bot.sendMessage(update.message.chat_id, message)


def help_handler(bot, update):
    bot.sendMessage(update.message.chat_id, help_message)


def error_handler(bot, update, error):
    logger.warn('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TELEGRAM_API_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start_handler))
    updater.dispatcher.add_handler(CommandHandler('track', track_handler, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('help', help_handler))

    updater.dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
