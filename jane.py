import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import login

import telegram.ext
from telegram.ext import Updater

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
    update.message.reply_text('*Hi*, I\'m Jane, _your_ assistant <3!', parse_mode='Markdown')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('What do you need help with!!')


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


def unknown(update, context):
    '''Last handler. If the command is not understood, replies as so'''

    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry brother"
                                                                    ", I never study a level. "
                                                                    "Don't understand that command")


#########################################################################################################
#########################################################################################################
def alarm(context):
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Beep!')


def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue and stop current one if there is a timer already
        new_job = context.job_queue.run_once(alarm, due, context=chat_id)
        context.chat_data['job'] = new_job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def one_chunk(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(10)
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue and stop current one if there is a timer already


        new_job = context.job_queue.run_once(alarm, due, context=chat_id)
        context.chat_data['job'] = new_job

        update.message.reply_text('Timer successfully set for {} seconds!'.format(due))

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')

#def callback_minute(context: telegram.ext.CallbackContext):
#    context.bot.send_message(chat_id='@examplechannel',
#                             text='One message every minute')

#job_minute = j.run_repeating(callback_minute, interval=60, first=0)


def study_chunk(update, context):
    chat_id = update.message.chat_id
    try:
        no_of_chunks = int(context.args[0])
        print(no_of_chunks)
        counter = 1
        for i in range (no_of_chunks):
            if counter % 2 == 0:
                new_job = context.job_queue.run_once(alarm, 10, context=chat_id)
                context.chat_data['job'] = new_job
                update.message.reply_text('Take a break brah!'.format(10))
                print("sleep awhile for 10")
                context.sleep(10)

            else:
                new_job = context.job_queue.run_once(alarm, 20, context=chat_id)
                context.chat_data['job'] = new_job
                update.message.reply_text('Lets go for the grind!'.format(20))
                print("sleep awhile for 20")

                context.sleep(20)
            counter += 1

    except (IndexError, ValueError):
        update.message.reply_text('Not working bro')



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(login.token, use_context=True)
    j = updater.job_queue

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.commandhandler.html
    # Handler class listening for telegram commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on non - command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler("caps", caps))
    dp.add_handler(InlineQueryHandler(inline_caps))

    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    dp.add_handler(CommandHandler("one_chunk", one_chunk,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    dp.add_handler(CommandHandler("study_chunk", study_chunk,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    dp.add_handler(MessageHandler(Filters.command, unknown))

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