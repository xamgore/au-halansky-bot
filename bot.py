#!/usr/bin/env python3
from telegram.ext import Updater, MessageHandler
from filter import halansky_filter
from actions import action_send_email
from config import env
from mailer import *

bot = Updater(env['TM_TOKEN'])
bot.dispatcher.add_handler(MessageHandler(halansky_filter, action_send_email))
bot.dispatcher.add_error_handler(print)
bot.start_polling()
bot.idle()
