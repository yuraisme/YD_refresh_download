# Используем официальный Python-образ
FROM python:3.13-slim


# Устанавливаем рабочую директорию и копируем
WORKDIR /app
COPY . /app/

# Устанавливаем Poetry
ENV POETRY_VERSION=1.5.1
RUN pip install "poetry==$POETRY_VERSION"

# Отключаем создание виртуальных окружений Poetry (используем системные зависимости)
ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1



# Устанавливаем зависимости
RUN poetry install --no-root

# Указываем команду для запуска приложения
CMD ["python3", "main.py"]
