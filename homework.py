import datetime
import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRAKTIKUM_TOKEN = os.environ.get('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

yabot = telegram.Bot(TELEGRAM_TOKEN)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(lineno)s %(message)s')

log = logging.getLogger('__name__')


def parse_homework_status(homework):
    statuses = {
        'reviewing': 'Работа взята в ревью',
        'rejected': 'К сожалению в работе нашлись ошибки.',
        'approved': ('Ревьюеру всё понравилось, можно '
                     'приступать к следующему уроку.'),
    }
    try:
        homework_name = homework['homework_name']
        verdict = statuses[homework['status']]
        return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'
    except KeyError:
        return 'Неверный ответ сервера'


def get_homework_statuses(current_timestamp):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    if current_timestamp is None:
        current_timestamp = get_UTC_stamp()

    try:
        homework_statuses = requests.get(url,
                                         headers={
                                             'Authorization':
                                             f'OAuth {PRAKTIKUM_TOKEN}'},
                                         params={'from_date':
                                                 current_timestamp})
    except requests.RequestException as e:  # не уверен что этот нужен
        error_report(f'При выполнении запроса произолша ошибка: {e}')
        return None
    except requests.HTTPError as e:
        error_report(f'При выполнении запроса произолша ошибка: {e}')
        return None

    json = homework_statuses.json()
    if 'message' in json:
        error_report('API error: ' + json.get('message') + json)
    log.debug(json)
    return json


def send_message(message, bot_client=None):
    """ Отправляет сообщение от бота по умолчанию или переданного """
    if not bot_client:
        bot_client = yabot
    return bot_client.send_message(CHAT_ID, message)


def error_report(message):
    """ Отправляет сообщение об ошибке в нужные места """
    log.error(message)
    send_message(message)


def get_UTC_stamp(year=None, month=None, day=None):
    """ отдает timestamp в UTC, можно подставить свое для дебага """
    if not (year and month and day):
        return int(time.time())

    dt = datetime.date(year, month, day)
    return int(time.mktime(dt.timetuple()))


def main():
    # проинициализировать бота здесь
    current_timestamp = get_UTC_stamp()  # начальное значение timestamp

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
                error_report(msg_err)

            # обновить timestamp, поскольку до этого момента данные уже есть
            current_timestamp = new_homework.get('current_date',
                                                 current_timestamp)
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            err_msg = f'Бот столкнулся с ошибкой: {e}'
            error_report(err_msg)
            time.sleep(60)


if __name__ == '__main__':
    main()
