import os
import time
from decouple import config


# def get_repo_name(github_bot_url):
#     return github_bot_url.split('/')[-1].split('.')


NEW_REPO_NAME = 'bot'

def publish_bot(notify_callback):
    # stop docker
    notify_callback('Останавливаю старый docker контейнер...')
    command = 'docker stop $(docker ps -q)'
    # ЖДУ пока поправят requirements.txt
    os.system(command)
    notify_callback('Done!')
    notify_callback('Удаляю старые файлы бота...')
    github_bot_url = config('github_bot_url')
    # repo_name, _ = get_repo_name(github_bot_url)
    repo_name = NEW_REPO_NAME
    # удаляем папку которая уже есть
    command = f'rm -rf {repo_name}'
    os.system(command)
    notify_callback('Done!')

    notify_callback('Клонирую репозиторий {github_bot_url} (ветка main)...')
    # клонируем репозиторий
    command = f'git clone {github_bot_url} ./{repo_name}'
    os.system(command)
    notify_callback('Done!')
    # копируем секреты (файл config.py)
    notify_callback('Копирую секреты...')
    command = f'cp config.py {repo_name}'
    os.system(command)

    command = f'cp .env {repo_name}'
    os.system(command)
    notify_callback('Done!')
    # / ЖДУ пока поправят requirements.txt
    # JOKE
    notify_callback('Взламываю твою операционныую систему...')
    notify_callback('Шучу :)')

    notify_callback('Поднимаю postgres в docker...')
    command = f'docker compose -f ./{repo_name}/docker-compose.yml up -d --build'
    os.system(command)
    notify_callback('Done!')
    notify_callback('Жду ответа от базы данных...')
    time.sleep(10)
    notify_callback('Done!')
    # docker up build
    notify_callback('Поднимаю бота в docker...')
    command = 'docker compose up -d --build'
    os.system(command)
    notify_callback('Done!')


if __name__ == '__main__':
    publish_bot()