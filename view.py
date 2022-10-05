import logging
import uuid
from decouple import config, Csv
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from models import publish_bot

DEVELOPER_IDS = config('developer_ids', cast=Csv(int))

PUBLISH_COMMAND_NAME = 'publish'
PUBLISH_COMMAND = f'/{PUBLISH_COMMAND_NAME}'
PUBLISH_COMMAND_FOCUSED = f'"{PUBLISH_COMMAND}"'

QUESTION = 'QUESTION'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    message = f'Привет. Если ты разработчик или разработчица я помогу тебе опубликовать Dance Bot\n' \
              f'Для этого просто набери команду {PUBLISH_COMMAND_FOCUSED} \n' \
              f'Используй "/help" для справки'
    update.message.reply_text(message)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    message = f'{PUBLISH_COMMAND} - публикация бота (только для разработчиков) \n' \
              f'/start - запуск бота \n' \
              f'/help - помощь \n' \
              f'/secret - ?'
    update.message.reply_text(message)


def secret_command(update: Update, context: CallbackContext):
    message = 'Отгадай загадку: \n\n' \
              'Что нужно сделать для того чтобы:\n' \
              '1. Пирог не подгорел?\n' \
              '2. Человек не утонул?\n' \
              '3. Девушка не забеременела?\n' \
              '(Один и тот же ответ на все вопросы)'
    update.message.reply_text(message)
    return QUESTION

def question(update: Update, context: CallbackContext):
    answer = update.message.text
    true_answer = config('secret_ansver', default=str(uuid.uuid4()))
    if answer.lower() == true_answer.lower():
        message = 'Вау! Какая внимательность! Загадка отгадана!'
        update.message.reply_text(message)
    else:
        message = 'Ответ неверный :('
        update.message.reply_text(message)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Подумай и возвращайся. Я буду ждать', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def publish(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    from_user = update.message.from_user
    user_id = from_user['id']
    username = from_user['username']
    if user_id not in DEVELOPER_IDS:
        update.message.reply_text('Публиковать бота могут только разработчики :(')
    else:
        # result = publish_bot()
        result = True
        if result:
            update.message.reply_text('Published!')