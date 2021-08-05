# Homework status checker telegram bot

## Abstract
Working with Yandex.Praktikum API.
Bot checks status of homework `reviewing`, `rejected`, `approved` and send a message to telegram chat if got one of them.
The core library is [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Install
1. Install python 3.7 or later
2. Install dependencies `pip install -r requirements.txt`
3. Open telegram client and:
 - Use @BotFather to create new bot (command `/newbot`). You'll get token
 - Use @userinfobot and get `user ID`

## Usage
Manual run
1. Fill key-fields in `.env` file (use template) 
2. Run `python homework.py`
Docker run
Run `do`

API token here:
https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a

<=== Yandex.Praktikum ===>
### Sprint 8

Lesson at: [Яндекс.Практикум (yandex.ru)](https://praktikum.yandex.ru/learn/backend-developer/courses/2ae6af00-3ebe-4597-9264-22f984b32334/sprints/5834/topics/58866697-3f7b-4e68-9ca8-e26bfec6a738/lessons/bbe29723-7066-4b66-a701-1222b5de8ed7/)
