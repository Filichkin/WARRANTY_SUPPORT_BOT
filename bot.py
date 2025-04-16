import os
import time

import telebot


bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

users = {}
