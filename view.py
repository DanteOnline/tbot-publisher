import logging
from decouple import config, Csv
from telegram import Update
from telegram.ext import CallbackContext
from models import publish_bot

DEVELOPER_IDS = config('developer_ids', cast=Csv(int))

PUBLISH_COMMAND_NAME = 'publish'
PUBLISH_COMMAND = f'/{PUBLISH_COMMAND_NAME}'
PUBLISH_COMMAND_FOCUSED = f'"{PUBLISH_COMMAND}"'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    message = f'Привет. Если ты разработчик я помогу тебе опубликовать Dance Bot\n' \
              f'Для этого просто набери команду {PUBLISH_COMMAND_FOCUSED}'
    update.message.reply_text(message)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    message = f'Для публикации Dance Bot набери {PUBLISH_COMMAND_FOCUSED}'
    update.message.reply_text(message)


def publish(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    from_user = update.message.from_user
    user_id = from_user['id']
    username = from_user['username']
    if user_id not in DEVELOPER_IDS:
        update.message.reply_text('Публиковать бота могут только разработчики :(')
    else:
        result = publish_bot()
        if result:
            update.message.reply_text('Published!')