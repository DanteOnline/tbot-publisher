from decouple import config
from telegram.ext import Updater, CommandHandler
from view import start, help_command, publish

BOT_TOKEN = config('bot_token')


def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("publish", publish))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()