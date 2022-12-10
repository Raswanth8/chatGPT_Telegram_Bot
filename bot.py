import requests
import json
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


bot = telegram.Bot(token='BOT_TOKEN')
updater = Updater(token='BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

def send_message(message):
    message = requests.utils.quote(message)
    response = requests.get("http://localhost:5001/chat?q=" + message)
    return response.text

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm ChatGPT bot. I can chat with you. Type /help to know more.")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Type /start to start the conversation. Type /stop to stop the conversation.")

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bye! I hope we can talk again some day.")

def chat(update, context):
    message = update.message.text
    response = send_message(message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)

    chat_handler = MessageHandler(Filters.text & (~Filters.command), chat)
    dispatcher.add_handler(chat_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
