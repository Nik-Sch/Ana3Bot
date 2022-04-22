
from datetime import datetime
from time import sleep
from telegram.callbackquery import CallbackQuery
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          CallbackContext,
                          CallbackQueryHandler,
                          )
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.jobqueue import JobQueue
from telegram import (
    Update,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Message,
)
import os
import logging
from typing import (
    Any,
    List,
    Tuple,
    Union
)
import re

class MainBot:

    def getStuff(self, update: Update) -> Tuple[Union[int, str], Message]:
        message = None
        if update.edited_message:
            message = update.edited_message
        else:
            message = update.message
        return (update.effective_chat.id, message)

    def start(self, update: Update, context: CallbackContext):
        chat_id, message = self.getStuff(update)
        message.reply_text("I do nothing useful.")

    def handleMessage(self, update: Update, context: CallbackContext):
        chat_id, message = self.getStuff(update)
        regex = re.compile('.*Modul.*empfehlen.*', re.IGNORECASE)
        if regex.match(message.text):
            message.reply_text('Analysis 3 für Mathe. Hat zwar 10LP, ist aber recht spannend.', reply_to_message_id=message.message_id)
            logging.info(f'replied to message "{message.text}" from {chat_id}')


    def handleError(self, update: Any, context: CallbackContext):
        logging.exception('Telegram Error', exc_info=context.error)
        try:
            context.bot.send_message(update.effective_chat.id, text="Uh oh, something went wrong.\nIf you like you can tell @NikSch.")
        except:
            pass


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    bot = MainBot()

    TOKEN = os.environ.get('BOT_TOKEN')
    if TOKEN == None:
        raise TypeError('No bot token defined')

    updater = Updater(token=TOKEN, workers=1)
    dispatcher: Dispatcher = updater.dispatcher
    job_queue: JobQueue = dispatcher.job_queue

    commands = [
        ['start', bot.start, 'Start'],
    ]
    for name, fun, _ in commands:
        dispatcher.add_handler(CommandHandler(name, fun, run_async=True))
    updater.bot.set_my_commands([(name, desc) for name, _, desc in commands])

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, bot.handleMessage))

    dispatcher.add_error_handler(bot.handleError)

    updater.start_polling()
    updater.idle()

    logging.info('stopped')
