from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, Updater, CallbackQueryHandler, CommandHandler, ConversationHandler, CallbackContext

# Define constants for the different states of the conversation
FIRST_CHOICE, SECOND_CHOICE, THIRD_CHOICE = range(3)

# Define the function that will be called when the user clicks on the first button

# at every state, have an option called cancel that ends conversation if data == cancel's number. 

async def first_choice(update, context):
    # Define the text and options for the second set of buttons
    text = "Please choose one of the following options:"
    options = [
        [InlineKeyboardButton("Track Money 💰", callback_data=str(1))],
        [InlineKeyboardButton("Track Food Intake 😋", callback_data=str(2))],
        [InlineKeyboardButton("Cancel", callback_data=str(3))]
    ]
    # Create the keyboard markup with the options
    reply_markup = InlineKeyboardMarkup(options)
    # Send the message with the keyboard to the user
    await update.message.reply_text(text, reply_markup=reply_markup)
    # Change the state of the conversation to the second choice
    return SECOND_CHOICE

# Define the function that will be called when the user clicks on the second button
async def second_choice(update, context):
    # Get the option chosen by the user
    query = update.callback_query
    choice = int(query.data)

    # Define the text and options for the final set of buttons
    if choice == 1:
        text = "Tracking Money! Please choose one of the following:"
        options = [
            [InlineKeyboardButton("Credit", callback_data=str(1.1))],
            [InlineKeyboardButton("Debit", callback_data=str(1.2))],
            [InlineKeyboardButton("Cancel", callback_data=str(1.3))]
        ]
    elif choice == 2:
        text = "Tracking Food Intake! Please choose one of the following:"
        options = [
            [InlineKeyboardButton("Option 2.1", callback_data=str(2.1))],
            [InlineKeyboardButton("Option 2.2", callback_data=str(2.2))],
            [InlineKeyboardButton("Cancel", callback_data=str(2.3))]
        ]
    elif choice == 3:
        text = "You chose to cancel"
        # await update.message.reply_text("Conversation canceled.")
        await query.edit_message_text(text=text)#, reply_markup=reply_markup)
        return ConversationHandler.END
    
    # Create the keyboard markup with the options
    # Edit the message to show the new keyboard with the options
    # End the conversation
    reply_markup = InlineKeyboardMarkup(options)
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    # await update.message.reply_text(text, reply_markup=reply_markup)
    return THIRD_CHOICE

async def third_choice(update, context):
    query = update.callback_query
    choice = str(query.data)
    if choice == "1.1":
        text = "You chose to track credits. Please choose one of the following:"
        options = [
            [InlineKeyboardButton("Was it cash?", callback_data=str("1.1.1"))],
            [InlineKeyboardButton("Was it an online transaction", callback_data=str("1.1.2"))],
            [InlineKeyboardButton("Cancel", callback_data=str("1.1.3"))]
        ]
    elif choice == "1.2":
        text = "You chose to track debit expenses. Please choose one of the following:"
        options = [
            [InlineKeyboardButton("Did you pay using Cash?", callback_data=str("1.2.1"))],
            [InlineKeyboardButton("Did you pay using UPI?", callback_data=str("1.2.2"))],
            [InlineKeyboardButton("Did you pay using Card?", callback_data=str("1.2.3"))],
            [InlineKeyboardButton("Cancel", callback_data=str("1.2.4"))]
        ]
    elif choice == "1.3":
        text = "You chose to cancel"
        # await update.message.reply_text("Conversation canceled.")
        await query.edit_message_text(text=text)#, reply_markup=reply_markup)
        return ConversationHandler.END
    elif choice == "2.1":
        text = "You chose to track food intake. Please choose one of the following:"
        options = [
            [InlineKeyboardButton("Did you eat out?", callback_data=str("2.1.1"))],
            [InlineKeyboardButton("Did you cook?", callback_data=str("2.1.2"))],
            [InlineKeyboardButton("Cancel", callback_data=str("2.1.3"))]
        ]
    elif choice == "2.2":
        text = "You chose to track food intake. Please choose one of the following:"
        options = [
            [InlineKeyboardButton("Did you eat out?", callback_data=str("2.1.1"))],
            [InlineKeyboardButton("Did you cook?", callback_data=str("2.1.2"))],
            [InlineKeyboardButton("Cancel", callback_data=str("2.1.3"))]
        ]
    elif choice == "2.3":
        text = "You chose to cancel"
        await update.message.reply_text("Conversation canceled.")
        # await query.edit_message_text(text=text)#, reply_markup=reply_markup)
        return ConversationHandler.END
    reply_markup = InlineKeyboardMarkup(options)
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return ConversationHandler.END

async def fourth_choice(update, context):
    query = update.callback_query
    choice = str(query.data)
    if choice == "1.1.1":
        text = "You chose to track cash credits. Please choose one of the following:"
        # take a number from the user as input and print it in the console
        await update.message.reply_text("Please enter the amount you want to track")
        
        # options = [[InlineKeyboardButton("Cancel", callback_data=str("abc"))]]


# Define the function that will be called when the user cancels the conversation
async def cancel(update, context):
    # Inform the user that the conversation has been canceled
    # End the conversation
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END

# Define the main function that will create and run the bot

# async def main() -> None:
#     """Run the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token("TOKEN").build()

#     # on different commands - answer in Telegram
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("help", help_command))

#     # on non command i.e message - echo the message on Telegram
#     application.add_handler(InlineQueryHandler(inline_query))

#     # Run the bot until the user presses Ctrl-C
#     application.run_polling()
if __name__ == '__main__':
    # Create the updater and dispatcher
    # updater = Updater("6122563729:AAEBbAnIFYAeMczk6e3yfdS8zLI6OzCYL8Y")
    application = Application.builder().token("6122563729:AAEBbAnIFYAeMczk6e3yfdS8zLI6OzCYL8Y").build()
    # dispatcher = updater.dispatcher
    
    # application.add_handler(CommandHandler("start", first_choice))


    # Create the conversation handler with the different states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", first_choice)],
        states={
            FIRST_CHOICE: [CallbackQueryHandler(first_choice)],
            SECOND_CHOICE: [CallbackQueryHandler(second_choice)],
            THIRD_CHOICE: [CallbackQueryHandler(third_choice)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    # Add the conversation handler to the dispatcher
    # dispatcher.add_handler(conv_handler)
    application.add_handler(conv_handler)
    application.run_polling()
    # Start the bot
    # updater.start_polling()
    # updater.idle()

# Call the main function to run the bot
