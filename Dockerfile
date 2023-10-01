# Используем официальный образ Python
FROM python:3.10

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt

# Копируем приложение в контейнер
COPY ./ /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Запускаем сервер FastAPI при запуске контейнера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]