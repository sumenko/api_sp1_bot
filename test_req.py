import os
import requests
from dotenv import load_dotenv
import datetime
import time
from pprint import pprint
load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')


url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
headers = {
    'Authorization': f'OAuth {PRAKTIKUM_TOKEN}',
}
dt = datetime.date(2021,3,1)
unix_time = int(time.mktime(dt.timetuple()))

response = requests.get(url, headers=headers, params={'from_date': unix_time})
print(response.url)
pprint(response.json())