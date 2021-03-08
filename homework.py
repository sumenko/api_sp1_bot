import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRAKTIKUM_TOKEN = os.environ.get("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

yabot = telegram.Bot(TELEGRAM_TOKEN)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(lineno)s %(message)s')

log = logging.getLogger('__name__')


def parse_homework_status(homework):
    homework_name = homework['homework_name']
    if homework.get('status') == 'reviewing':
        return 'Работа взята в ревью.'

    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = ('Ревьюеру всё понравилось, можно '
                   'приступать к следующему уроку.')

    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'

    homework_statuses = requests.get(url,
                                     headers={
                                         'Authorization':
                                         f'OAuth {PRAKTIKUM_TOKEN}'},
                                     params={'from_date': current_timestamp})
    json = homework_statuses.json()
    if 'message' in json:
        err_msg = "API error: " + json.get('message')
        log.error(err_msg)
        send_message(err_msg)
    return json


def send_message(message, bot_client=None):
    if not bot_client:
        bot_client = yabot
    return bot_client.send_message(CHAT_ID, message)


def main():
    # проинициализировать бота здесь
    current_timestamp = int(time.time())  # начальное значение timestamp
    log.debug('Start watching homework')
    send_message('Start watching...')

    while True:
        try:
            # смотрим статус домашки начиная с текущего момента
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]), yabot)

            if 'error' in new_homework:
                msg_err = 'API error: {}'.format(
                    new_homework.get('error').get('error'))
                log.error(msg_err)
                send_message(msg_err)

            # обновить timestamp, поскольку до этого момента данные уже есть
            current_timestamp = new_homework.get('current_date',
                                                 current_timestamp)
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            err_msg = f'Бот столкнулся с ошибкой: {e}'
            log.error(err_msg)
            send_message(err_msg)
            time.sleep(5)


if __name__ == '__main__':
    main()
