# Codeforces Tasks Bot

Telegram бот для поиска задач на Codeforces по темам и сложности.

## Описание

Бот помогает пользователям находить задачи на Codeforces, фильтруя их по:

- Темам (например, "math", "dp", "graphs" и т.д.)
- Диапазону сложности (от 800 до 2600)

Бот автоматически обновляет базу данных задач каждый день в 3:00 по московскому времени.

## Технологии

- Python 3.8+
- PostgreSQL
- SQLAlchemy (асинхронный режим)
- aiogram 3.x
- APScheduler
- asyncpg

## Установка

1. Клонируйте репозиторий:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Создайте виртуальное окружение и активируйте его:

```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории проекта со следующими переменными:

```env
# Database
DB_USER=your_db_user
PASSWORD=your_db_password
HOST=localhost
PORT=5432
DATABASE=your_db_name

# Telegram Bot
TOKEN=your_bot_token
```

5. Создайте базу данных PostgreSQL и примените миграции:

```bash
# База данных будет создана автоматически при первом запуске
```

## Запуск

1. Активируйте виртуальное окружение (если еще не активировано):

```bash
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
```

2. Запустите бота:

```bash
python main.py
```

## Структура проекта

```
.
├── app/
│   ├── crud/           # CRUD операции
│   │   ├── problem_crud.py
│   │   └── tag_crud.py
│   ├── service/        # Сервисный слой
│   │   ├── problem_service.py
│   │   └── tag_service.py
│   ├── database.py     # Настройка БД
│   ├── fill_db.py      # Заполнение БД
│   └── models.py       # Модели SQLAlchemy
├── bot/
│   ├── bot.py          # Инициализация бота
│   ├── handlers.py     # Обработчики команд
│   ├── keyboards.py    # Клавиатуры
│   └── states.py       # Состояния FSM
├── constants.py        # Конфигурация
├── main.py            # Точка входа
└── requirements.txt   # Зависимости
```

## Использование

1. Запустите бота в Telegram
2. Отправьте команду `/start`
3. Выберите тему из предложенного списка
4. Выберите минимальную сложность
5. Выберите максимальную сложность
6. Получите список задач, соответствующих вашим критериям

## Особенности

- Асинхронная работа с базой данных
- Автоматическое обновление базы данных задач
- Удобный интерфейс с inline-клавиатурами
- Фильтрация задач по темам и сложности
- Случайный выбор задач из подходящих
