import logging
from typing import Dict
from telegram import __version__ as TG_VER
import requests
from config import app_id, app_key
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

BASE_CHOOSING, BASE_EXPENSE, BASE_WATER, CREDIT_EXPENSE_BASE, DEBIT_EXPENSE_BASE, CASH_EXPENSE_BASE, EXPENSE_VALUE, RECIEVED_EXPENSE_VALUE, RECIEVED_PURSPOSE, FOOD_NAME, GET_CALORIES, RECIEVED_CALORIES, RECIVED_FOOD_NAME, GET_FOOD_NAME = range(14)

"""
KEYBOARD MARKUPS
"""

base_keyboard = [['Food', 'Expenses'], ['Activity', 'Water'], ['Stop Tracking']]
base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=True)

expense_type_keyboard = [['Credit', 'Debit'], ['Cash'], ["Go Back"]]
expense_type_markup = ReplyKeyboardMarkup(expense_type_keyboard, one_time_keyboard=True)

credit_expense_keyboard = [["Utility", "Food"], ["Shopping", "Other"], ["Go Back"]]
credit_expense_markup = ReplyKeyboardMarkup(credit_expense_keyboard, one_time_keyboard=True)

debit_expense_keyboard = [["Utility", "Food"], ["Shopping", "Other"], ["Go Back"]]
debit_expense_markup = ReplyKeyboardMarkup(debit_expense_keyboard, one_time_keyboard=True)

cash_expense_keyboard = [["Utility", "Food"], ["Shopping", "Other"], ["Go Back"]]
cash_expense_markup = ReplyKeyboardMarkup(cash_expense_keyboard, one_time_keyboard=True)

water_intake_keyboard = [['1', '2'], ['3', '4'], ["Go Back"]]
water_intake_markup = ReplyKeyboardMarkup(water_intake_keyboard, one_time_keyboard=True)

know_calories_keyboard = [['Yes', 'No'], ["Go Back"]]
know_calories_markup = ReplyKeyboardMarkup(know_calories_keyboard, one_time_keyboard=True)

"""
VARIABLES
"""
global latest_expense
expense_type = None

"""
BASE FUNCTIONS
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "What do you want to track?", reply_markup=base_markup)
    return BASE_CHOOSING

def update_database(tracking_data):
    if tracking_data['type'] == 'expense':
        print("Expense")
    elif tracking_data['type'] == 'water':
        print("Water")
    elif tracking_data['type'] == 'food':
        print("Food")
    elif tracking_data['type'] == 'activity':
        print("Activity")

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
        f"Tracking Done!", reply_markup=ReplyKeyboardRemove()
    )
    # user_data.clear()
    print(context.user_data)
    return ConversationHandler.END


"""
FOOD
"""
# async def food_base(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     await update.message.reply_text(
#         "How much did you spend?"
#     )
#     return FOOD_NAME

async def know_calories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # BASE_CHOOSING
    await update.message.reply_text(
        "Do you know the number of calories?", reply_markup=know_calories_markup
    )
    return GET_CALORIES

async def get_calories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # GET_CALORIES
    await update.message.reply_text(
        "How many calories did you eat?"
    )
    return RECIEVED_CALORIES

async def store_food_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # GET_FOOD_NAME
    food_name = update.message.text
    context.user_data['food_name'] = food_name
    global latest_food
    latest_food = food_name
    # if context.user_data['calories']:
    if 'calories' in context.user_data:
        await update.message.reply_text(
        f"Added {food_name} to your food. Calories: {context.user_data['calories']}"
        )
    else:
        url = f'https://api.edamam.com/api/food-database/v2/parser?ingr={food_name}&app_id={app_id}&app_key={app_key}'
        response = requests.get(url)
        data = response.json()
        calories = data['hints'][0]['food']['nutrients']['ENERC_KCAL']
        # quantity = data['hints'][0]['measures'][0]['label']
        await update.message.reply_text(
        f"Added {food_name} to your food. Calories: {calories}"
        )
    return ConversationHandler.END

async def user_entered_calories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # RECIEVED_CALORIES 
    calories = update.message.text
    calories = int(calories)
    context.user_data['calories'] = calories
    await update.message.reply_text(
        "What did you have?"
    )
    return GET_FOOD_NAME

# async def calculate_calories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:



"""
COMMON EXPENSE
"""
async def expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "What type of expense?", reply_markup=expense_type_markup
    )
    return BASE_EXPENSE

async def get_expense_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "How much did you spend?"
    )
    return EXPENSE_VALUE

async def store_expense_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    amount = update.message.text
    amount = int(amount)
    context.user_data['amount'] = amount
    global latest_expense
    latest_expense = amount
    try:
        await update.message.reply_text(
            f"Added {amount} to your expense. What was the purpose?"
        )
    except:
        await update.message.reply_text(
            "Please enter a valid number"
        )
    return RECIEVED_EXPENSE_VALUE

async def get_purpose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    purpose = str(update.message.text)
    await update.message.reply_text(
        f"Added {latest_expense} to your expense for {purpose}.\nClosing Tracker",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['purpose'] = purpose
    context.user_data['tracked'] = 'expense'
    print(context.user_data)
    return ConversationHandler.END


"""
CREDIT SPECIFIC
"""
async def credit_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['expense_type'] = 'credit'
    await update.message.reply_text(
        "What type of credit expense?", reply_markup=credit_expense_markup
    )
    return CREDIT_EXPENSE_BASE


"""
DEBIT SPECIFIC
"""
async def debit_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['expense_type'] = 'debit'
    await update.message.reply_text(
        "What type of debit expense?", reply_markup=debit_expense_markup
    )
    return DEBIT_EXPENSE_BASE



"""
CASH SPECIFIC
"""
async def cash_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['expense_type'] = 'cash'
    await update.message.reply_text(
        "What type of cash expense?", reply_markup=cash_expense_markup
    )
    return CASH_EXPENSE_BASE



async def water(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "How much water did you drink today?", reply_markup=water_intake_markup
    )
    context.user_data['tracked'] = 'water'
    return BASE_WATER


"""
MAIN
"""
def main() -> None:
    application = Application.builder().token("6122563729:AAEBbAnIFYAeMczk6e3yfdS8zLI6OzCYL8Y").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states = {
            BASE_CHOOSING: [
                MessageHandler(filters.Regex("^Food$"), know_calories),
                MessageHandler(filters.Regex("^Expenses$"), expense),
                MessageHandler(filters.Regex("^Activity$"), done),
                MessageHandler(filters.Regex("^Water$"), water),
                MessageHandler(filters.Regex("^Stop Tracking$"), done),
            ],
            BASE_EXPENSE: [
                MessageHandler(filters.Regex("^Credit$"), credit_expense),
                MessageHandler(filters.Regex("^Debit$"), debit_expense),
                MessageHandler(filters.Regex("^Cash$"), cash_expense),
                MessageHandler(filters.Regex("^Go Back$"), start),
            ],
            BASE_WATER: [
                MessageHandler(filters.Regex("^1$"), done),
                MessageHandler(filters.Regex("^2$"), done),
                MessageHandler(filters.Regex("^3$"), done),
                MessageHandler(filters.Regex("^4$"), done),
                MessageHandler(filters.Regex("^Go Back$"), start),
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
            CASH_EXPENSE_BASE: [
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
            GET_CALORIES: [
                    MessageHandler(filters.Regex("^Yes$"), get_calories),
                    MessageHandler(filters.Regex("^No$"), store_food_info),
                    MessageHandler(filters.Regex("^Go Back$"), start)
                ],
            GET_FOOD_NAME: [
                    MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), store_food_info)
                ],
            RECIEVED_CALORIES: [
                    MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), user_entered_calories)    
                ],
                },
        fallbacks = [MessageHandler(filters.Regex("^Done$"), done)],
    )    

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()