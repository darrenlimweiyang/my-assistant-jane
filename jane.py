import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import login

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# allows me to log messages. Basically the above code tells me when someone logs in
# loggin helps to tell me where and why things don't work

logger = logging.getLogger(__name__)


# https://stackoverflow.com/questions/50714316/how-to-use-logging-getlogger-name-in-multiple-modules
# tldr, the logger = above is used to get the hierarchy of which the logger is at. Eg. if we used multiple modules


# Defining command handlers
# Takes in the command update and context
# update and context - what do they mean?
#
# Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('*Fuck* _your_ mother!', parse_mode='Markdown')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help lanjiao!')


def echo(update, context):
    """Echo the user message."""
    print(update.message.text)
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

'''
def upper_case(update, context):
    """Lower cases the message"""
    update.message.reply_text(update.message.text.upper())
'''

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def inline_caps(update, context):
    '''
    Addition of inline mode
    This means that the bot can be called in a chat/group chat
    Great as the functions can be used without even triggering the bot.
    Immediate use cases would be CAP text, converting to code
    Tougher use cases would be sending your schedule etc
    '''
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(login.token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.commandhandler.html
    # Handler class listening for telegram commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler("caps", caps))
    dp.add_handler(InlineQueryHandler(inline_caps))
    #dp.add_handler(MessageHandler("loud", upper_case))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
