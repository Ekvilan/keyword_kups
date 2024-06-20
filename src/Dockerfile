# Используйте базовый образ, например, официальный образ Python
FROM python:3.8-slim

# Установите cron и любые другие необходимые пакеты
RUN apt-get update && apt-get install -y cron

# Скопируйте ваши скрипты в контейнер
COPY main.py /usr/src/app/main.py
COPY schemas.py /usr/src/app/schemas.py

# Дайте права на выполнение скриптам
RUN chmod +x /usr/src/app/main.py
RUN chmod +x /usr/src/app/schemas.py

# Создайте файл crontab с расписанием запуска скриптов
RUN echo "0 10 * * * /usr/src/app/main.py" > /etc/cron.d/mycron
RUN echo "30 10 * * 2 /usr/src/app/schemas.py" >> /etc/cron.d/mycron

# Дайте права на файл crontab и установите его
RUN chmod 0644 /etc/cron.d/mycron
RUN crontab /etc/cron.d/mycron

# Запустите cron в фоновом режиме
CMD ["cron", "-f"]