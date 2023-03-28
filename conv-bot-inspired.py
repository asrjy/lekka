import logging
from typing import Dict
from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_CHOOSING, BASE_EXPENSE, BASE_WATER, CREDIT_EXPENSE_BASE, DEBIT_EXPENSE_BASE, EXPENSE_VALUE, RECIEVED_EXPENSE_VALUE, RECIEVED_PURSPOSE = range(8)

base_keyboard = [['Food', 'Expenses'], ['Activity', 'Water']]
base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=True)

expense_type_keyboard = [['Credit', 'Debit'], ['Cash']]
expense_type_markup = ReplyKeyboardMarkup(expense_type_keyboard, one_time_keyboard=True)

credit_expense_keyboard = [["Utility", "Food"], ["Shopping", "Other"], ["Go Back"]]
credit_expense_markup = ReplyKeyboardMarkup(credit_expense_keyboard, one_time_keyboard=True)

debit_expense_keyboard = [["Utility", "Food"], ["Shopping", "Other"], ["Go Back"]]
debit_expense_markup = ReplyKeyboardMarkup(debit_expense_keyboard, one_time_keyboard=True)

water_intake_keyboard = [['1', '2'], ['3', '4']]
water_intake_markup = ReplyKeyboardMarkup(water_intake_keyboard, one_time_keyboard=True)

latest_expense = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "What do you want to track?", reply_markup=base_markup)
    return BASE_CHOOSING

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    # user_data = context.user_data
    # if "choice" in user_data:
    #     del user_data["choice"]

    # await update.message.reply_text(
    #     f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
    #     reply_markup=ReplyKeyboardRemove(),
    # )
    await update.message.reply_text(
        f"I have tracked shit today", reply_markup=ReplyKeyboardRemove()
    )
    # user_data.clear()
    return ConversationHandler.END

async def expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "What type of expense?", reply_markup=expense_type_markup
    )
    return BASE_EXPENSE

async def credit_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "What type of credit expense?", reply_markup=credit_expense_markup
    )
    return CREDIT_EXPENSE_BASE

async def debit_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "What type of debit expense?", reply_markup=debit_expense_markup
    )
    return DEBIT_EXPENSE_BASE

async def get_expense_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "How much did you spend?"
    )
    return EXPENSE_VALUE

async def store_expense_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    amount = update.message.text
    amount = int(amount)
    # store this value in latest_expense variable 
    latest_expense = amount
    await update.message.reply_text(
        f"Added {amount} to your expense. What was the purpose?"
    )
    return RECIEVED_EXPENSE_VALUE

async def get_purpose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    purpose = str(update.message.text)
    await update.message.reply_text(
        f"Added {latest_expense} to your expense for {purpose}."
    )
    return RECIEVED_EXPENSE_VALUE

async def water(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "How much water did you drink today?", reply_markup=water_intake_markup
    )
    return BASE_WATER

def main() -> None:
    application = Application.builder().token("6122563729:AAEBbAnIFYAeMczk6e3yfdS8zLI6OzCYL8Y").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states = {
            BASE_CHOOSING: [
                MessageHandler(filters.Regex("^Food$"), done),
                MessageHandler(filters.Regex("^Expenses$"), expense),
                MessageHandler(filters.Regex("^Activity$"), done),
                MessageHandler(filters.Regex("^Water$"), water),
            ],
            BASE_EXPENSE: [
                MessageHandler(filters.Regex("^Credit$"), credit_expense),
                MessageHandler(filters.Regex("^Debit$"), debit_expense),
                MessageHandler(filters.Regex("^Cash$"), done),
            ],
            BASE_WATER: [
                MessageHandler(filters.Regex("^1$"), done),
                MessageHandler(filters.Regex("^2$"), done),
                MessageHandler(filters.Regex("^3$"), done),
                MessageHandler(filters.Regex("^4$"), done),
            ],
            CREDIT_EXPENSE_BASE: [
                MessageHandler(filters.Regex("^Utility$"), get_expense_value),
                MessageHandler(filters.Regex("^Food$"), get_expense_value),
                MessageHandler(filters.Regex("^Shopping$"), get_expense_value),
                MessageHandler(filters.Regex("^Other$"), get_expense_value),
                MessageHandler(filters.Regex("^Go Back$"), expense),
            ],
            DEBIT_EXPENSE_BASE: [
                MessageHandler(filters.Regex("^Utility$"), get_expense_value),
                MessageHandler(filters.Regex("^Food$"), get_expense_value),
                MessageHandler(filters.Regex("^Shopping$"), get_expense_value),
                MessageHandler(filters.Regex("^Other$"), get_expense_value),
                MessageHandler(filters.Regex("^Go Back$"), expense),
                ],
            EXPENSE_VALUE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), store_expense_value
                )],
            RECIEVED_EXPENSE_VALUE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), get_purpose)
                ],
            RECIEVED_PURSPOSE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), done)
                ],
                },
        fallbacks = [MessageHandler(filters.Regex("^Done$"), done)],
    )    

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()