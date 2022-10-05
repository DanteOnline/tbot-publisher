import os
from decouple import config


# def get_repo_name(github_bot_url):
#     return github_bot_url.split('/')[-1].split('.')


NEW_REPO_NAME = 'bot'

def publish_bot():
    # stop docker
    command = 'docker stop $(docker ps -q)'
    # ЖДУ пока поправят requirements.txt
    os.system(command)
    github_bot_url = config('github_bot_url')
    # repo_name, _ = get_repo_name(github_bot_url)
    repo_name = NEW_REPO_NAME
    # удаляем папку которая уже есть
    command = f'rm -r {repo_name}'
    os.system(command)

    # клонируем репозиторий
    command = f'git clone {github_bot_url} ./{repo_name}'
    os.system(command)
    # копируем секреты (файл config.py)
    command = f'cp config.py {repo_name}'
    os.system(command)
    # / ЖДУ пока поправят requirements.txt
    # docker up build
    command = 'docker compose up -d --build'
    os.system(command)
    return True


if __name__ == '__main__':
    publish_bot()