import os
import time
import datetime

import logging
import requests
import telegram
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
yabot = telegram.Bot(TELEGRAM_TOKEN)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(lineno)s %(message)s")
log = logging.getLogger('__name__')
"""
Бот должен логировать момент своего запуска (уровень DEBUG),
каждую отправку сообщения (уровень INFO) и отправлять сообщения
уровня ERROR вам в Телеграм.
"""
def parse_homework_status(homework):
    homework_name = homework['homework_name']
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = ('Ревьюеру всё понравилось, можно'
                   'приступать к следующему уроку.')
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'

# Вход
def get_homework_statuses(current_timestamp):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    
    homework_statuses = requests.get(url, 
                                     headers={
                                              'Authorization':
                                              f'OAuth {PRAKTIKUM_TOKEN}'
                                             },
                                     params={'from_date': current_timestamp})
    return homework_statuses.json()
    

def send_message(message, bot_client):
    log.info('send message: ' + message)
    return bot_client.send_message(CHAT_ID, message)


def main():
    # проинициализировать бота здесь
    current_timestamp = int(time.time())  # начальное значение timestamp
    log.debug('Bot start watching')
    send_message('Bot start watching', yabot)
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]), yabot)
            
            # обновить timestamp
            current_timestamp = new_homework.get('current_date', 
                                                 current_timestamp)  
            # time.sleep(300)  # опрашивать раз в пять минут
            time.sleep(5)  # опрашивать раз в пять минут

        except Exception as e:
            log.error(f'Бот столкнулся с ошибкой: {e}')

            time.sleep(5)


if __name__ == '__main__':
    main()
