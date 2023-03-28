import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CHOOSING, OPTION1, OPTION2 = range(3)

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a baot, please talk to me!")

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Option 1", callback_data=str(OPTION1))],
        [InlineKeyboardButton("Option 2", callback_data=str(OPTION2))]
    ])
    update.message.reply_text("Choose an option:", reply_markup=reply_markup)
    return CHOOSING


def option_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    option = int(query.data)

    if option == OPTION1:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Option 1-A", callback_data="1-A")],
            [InlineKeyboardButton("Option 1-B", callback_data="1-B")]
        ])
        query.edit_message_text(text="You chose option 1. Choose another option:", reply_markup=reply_markup)
        return 'OPTION1'
    elif option == OPTION2:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Option 2-A", callback_data="2-A")],
            [InlineKeyboardButton("Option 2-B", callback_data="2-B")]
        ])
        query.edit_message_text(text="You chose option 2. Choose another option:", reply_markup=reply_markup)
        return 'OPTION2'
    
def option_chosen_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    option = query.data

    # Do something with the selected option
    query.edit_message_text(text=f"You chose {option}. Thanks for playing!")

    return ConversationHandler.END

def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.edit_message_text(text = 'Cancelled.')
    return ConversationHandler.END

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text_caps = ' '.join(context.args).upper()
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# async def aut(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # text_caps = ' '.join(context.args).upper()
#     # this will return text with alternative letter in upper case and lower case
#     text_caps = ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(' '.join(context.args))])
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

if __name__ == '__main__':
    application = ApplicationBuilder().token('6122563729:AAEBbAnIFYAeMczk6e3yfdS8zLI6OzCYL8Y').build()
    # updater = Updater('6122563729:AAEBbAnIFYAeMczk6e3yfdS8zLI6OzCYL8Y', update_queue=False)
    # FIxing Updater object has no attribute 'dispatcher'

    # application = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [CallbackQueryHandler(option_chosen)],
            OPTION1: [CallbackQueryHandler(option_chosen_again)],
            OPTION2: [CallbackQueryHandler(option_chosen_again)]
        },
        fallbacks=[CallbackQueryHandler(cancel)]
        # CallbackQueryHandler(cancel)

    )

    application.add_handler(conv_handler)


            

    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    # start_handler = CommandHandler('start', start)
    # caps_handler = CommandHandler('caps', caps)
    # aut_handler = CommandHandler('aut', aut)
    

    # application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    # application.add_handler(caps_handler)
    # application.add_handler(aut_handler)
    
    application.run_polling()
    application.idle()