import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a baot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def aut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # text_caps = ' '.join(context.args).upper()
    # this will return text with alternative letter in upper case and lower case
    text_caps = ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(' '.join(context.args))])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

if __name__ == '__main__':
    application = ApplicationBuilder().token('6122563729:AAEBbAnIFYAeMczk6e3yfdS8zLI6OzCYL8Y').build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    aut_handler = CommandHandler('aut', aut)
    

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(aut_handler)
    
    application.run_polling()