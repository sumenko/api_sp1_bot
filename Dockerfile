FROM python:3.8.5-slim
LABEL name='Yandex praktikum homework bot' author='Sumenko V'
RUN mkdir /code
COPY requirements.txt /code
RUN pip3 install -r /code/requirements.txt
COPY . /code
CMD python /code/homework.py


