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
    filename='main.log',
    encoding='utf-8',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    message = f'Привет. Если ты разработчик или разработчица я помогу тебе опубликовать Dance Bot\n' \
              f'Для этого просто набери команду {PUBLISH_COMMAND_FOCUSED} \n' \
              f'Используй "/help" для справки'
    from_user = update.message.from_user
    user_id = from_user['id']
    username = from_user['username']
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
    from_user = update.message.from_user
    user_id = from_user['id']
    username = from_user['username']
    answer = update.message.text
    true_answer = config('secret_ansver', default=str(uuid.uuid4()))
    if answer.lower() == true_answer.lower():
        message = 'Вау! Какая внимательность! Загадка отгадана!'
        update.message.reply_text(message)
        logger.info(f'Question solved by {user_id} {username}')
    else:
        logger.info(f'Wrong answer "{answer}" by {user_id} {username}')
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
    logger.info(f'Start publish bot {user_id} {username}')
    if user_id not in DEVELOPER_IDS:
        update.message.reply_text('Публиковать бота могут только разработчики :(')
        logger.info('Unauthorized try')
    else:
        try:
            logger.info('Start publish bot')
            help_text = 'Операция может занять некоторое время (ждите :)). ' \
                        'Если всё будет хорошо - придет сообщение "Published!"' \
                        'Если нет - придет текст ошибки'
            update.message.reply_text(help_text)
            publish_bot(notify_callback=update.message.reply_text)
        except Exception as e:
            update.message.reply_text('ОШИБКА!')
            update.message.reply_text(e.__class__.__name__)
            update.message.reply_text(str(e))
            logger.error(f'{e.__class__.__name__}: {e}')
        else:
            update.message.reply_text('Published!')
            logger.info('Bot published')