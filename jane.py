from __future__ import print_function
import logging
import test_func
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import login
import time
import datetime as dt
from datetime import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


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

##############################
# What is update and context #
##############################
# From printing, we note that update is a json file detailing all the details of the bot.
# Every update refers to an individual object from someone that texted the bot
# for context, it refers to telegram.ext.callbackcontext.CallbackContext object at 0x107581b00
# Some sort of object.


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


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
    print("bro")
    context.bot.send_message(job.context, text='Yo take a break!')


def getting_events(update, context):
    """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
    days_of_week = ("ISO Week days start from 1",
                     "Monday",
                     "Tuesday",
                     "Wednesday",
                     "Thursday",
                     "Friday",
                     "Saturday",
                     "Sunday" )
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = dt.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=5, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event = (start, event['summary'])

        event_start = datetime.strptime(event[0].split("T")[1].split("+")[0], "%H:%M:%S").strftime("%I:%M %p")
        datetime_obj = datetime.strptime(event[0].split("T")[0], '%Y-%M-%d')
        week_day = days_of_week[datetime_obj.isoweekday()]
        update.message.reply_text("For *{}*, ".format(week_day) + "\n"
                                  "    {} starts at {}".format(event[1], event_start), parse_mode='Markdown')


'''
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
        new_job = context.job_queue.run_once(alarm(due), due, context=chat_id)
        context.chat_data['job'] = new_job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')
'''


def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Timer successfully unset!')

'''
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
'''


def study_chunk(update, context):
    chat_id = update.message.chat_id
    try:
        no_of_chunks = int(context.args[0])
        t = time.localtime()
        current_time = time.strftime("%H:%M", t)
        update.message.reply_text('You have chosen to have {} study chunks. Starting now @ {}.'.format(no_of_chunks,
                                                                                                       current_time))
        for i in range(1,no_of_chunks+1):
            t = time.localtime()
            current_time = time.strftime("%H:%M", t)
            update.message.reply_text('Please begin chunk #{} now @ {}'.format(i, current_time))
            time_for_study = 60 * 25
            time_for_break = 60 * 5
            time.sleep(time_for_study)
            t = time.localtime()
            current_time = time.strftime("%H:%M", t)
            update.message.reply_text('You have completed chunk number {} at {}'.format(i, current_time))
            update.message.reply_text('Please take your {} break now for 5 minutes.'.format(i))
            time.sleep(time_for_break)
            update.message.reply_text('Your break has ended at {}. Please get back to work.'.format(current_time))
            update.message.reply_text('----\n')

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
    dp.add_handler(CommandHandler("start", test_func.start))
    dp.add_handler(CommandHandler("help", test_func.help))

    # on non - command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, test_func.echo))
    dp.add_handler(CommandHandler("caps", test_func.caps))
    dp.add_handler(InlineQueryHandler(inline_caps))

    '''dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))'''
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    dp.add_handler(CommandHandler("study_chunk", study_chunk,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    dp.add_handler(CommandHandler("today_schedule", getting_events))

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
