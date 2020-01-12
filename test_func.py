from __future__ import print_function
import logging
import test_func
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import login
import time
from datetime import datetime
import pickle
import os.path
from googleapiclient.discovery import build

def start(update, context):
    """Send a message when the command /start is issued."""
    print(update)
    print("\n")
    print(context)
    update.message.reply_text('*Hi*, I\'m Jane, _your_ assistant <3!', parse_mode='Markdown')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('What do you need help with!!')


def echo(update, context):
    """Echo the user message."""
    print(update.message.text)
    update.message.reply_text(update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)