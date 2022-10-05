from decouple import config
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from view import start, help_command, publish, secret_command, question, QUESTION, cancel

BOT_TOKEN = config('bot_token')


def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("publish", publish))
    # dispatcher.add_handler(CommandHandler("secret", secret_command))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('secret', secret_command)],
        states={
            QUESTION: [MessageHandler(Filters.text & ~Filters.command, question)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()