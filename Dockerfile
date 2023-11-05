# Используйте официальный образ Python
FROM python:3.8

# Создайте рабочую директорию
WORKDIR /app

# Копируйте ваш скрипт Python и требуемые файлы
COPY jira.py /app/
COPY requirements.txt /app/
COPY config.yaml /app/

# Установите зависимости
RUN pip install -r requirements.txt

# Установите matplotlib, чтобы графики работали внутри контейнера
RUN apt-get update && apt-get install -y python3-tk

# Запустите ваш скрипт
CMD ["python", "jira.py"]
