FROM python:3.9-slim

# Установка poetry
RUN pip install poetry==1.8.5

# Копирование кода приложения
COPY . .

# Установка зависимостей с помощью poetry
RUN poetry install --no-dev

# Установка рабочей директории
WORKDIR /app

# Выполнение команды для запуска приложения
CMD ["poetry", "run", "start"]
