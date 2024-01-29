from __future__ import print_function

import socket
import logging
import requests

from django.conf import settings

logger = logging.getLogger('nextgis_common.telegram')


class SimpleTelegramBot:

    API_URL = 'https://api.telegram.org/'

    def __init__(self, bot_id):
        self.bot_id = bot_id

    @property
    def bot_url(self):
        return self.API_URL + 'bot%s' % self.bot_id

    def command_url(self, command):
        return self.bot_url + '/' + command

    def send_message(self, chat_id, message, parse_mode='HTML'):
        url = self.command_url('sendMessage')
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': parse_mode
        }
        try:
            requests.post(url, data=data)
        except requests.RequestException as e:
            logger.error("SimpleTelegramBot exception: %s" % e)


def construct_message(html_msg, add_header=True, add_separators=True):
    message = ''
    separator = '-' * 36

    if add_header:
        if hasattr(settings, 'TELEGRAM_MSG_HEADER'):
            header = settings.TELEGRAM_MSG_HEADER
        else:
            header = socket.getfqdn()
            header += ' (dev)' if settings.DEBUG else ''

        message += '<b>%s</b>\n%s\n' % (header, separator)
        if add_separators:
            message += separator

    if isinstance(html_msg, list):
        html_msg_parts = html_msg
    else:
        html_msg_parts = [html_msg]

    if add_separators:
        separator_with_new_lines = '\n%s\n' % separator
        message += separator_with_new_lines.join(html_msg_parts)
    else:
        message += ' '.join(html_msg_parts)

    return message


def send_message(html_msg, add_header=True, add_separators=False):
    if not hasattr(settings, 'TELEGRAM_TOKEN') or not hasattr(settings, 'TELEGRAM_CHAT_ID'):
        return

    if settings.TELEGRAM_TOKEN is None:
        return
    if settings.TELEGRAM_CHAT_ID is None:
        return

    bot = SimpleTelegramBot(settings.TELEGRAM_TOKEN)

    if getattr(settings, 'TELEGRAM_PRINT_ONLY', False):
        print(construct_message(html_msg))
        return

    bot.send_message(
        settings.TELEGRAM_CHAT_ID,
        construct_message(html_msg, add_header, add_separators)
    )
