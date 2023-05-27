## Телеграм бот "Гибкий календарь"
[![Basic validation](https://github.com/actions/labeler/actions/workflows/basic-validation.yml/badge.svg?branch=main)](https://github.com/Lascor22/flex_calendar/actions/workflows/python-app.yml)
### Использование
Гибкий календарь позволит вам структурировать все ваши дела в календаре.  
Он позволяет создавать, удалять и смотреть события, а также соотносить их с календарем.  
Ссылка на бот: https://t.me/flexCalendarBot

### Установка
1. Скачиваем Python https://www.python.org/downloads/
2. Скачиваем код `git clone https://github.com/Lascor22/flex_calendar.git`
3. Скачиваем зависимости: 
```sh
pip install telebot python-telegram-bot-calendar
```
4. Устанавливаем переменные окружения:
    - `API_TELEGRAM_TOKEN` - токен телеграм бота
    - `GRAFANA_TOKEN` - токен Grafana
    - `GRAFANA_USER_ID` - идентификатор пользователя в Grafana
5. запускаем `python bot.py --log_file=<путь до файлов с логами> --database=<путь до базы данных>`
### Использованные технологии
Для разработки данного программного продукта были использованы следующие технологии:
- база данных *SQLite* для хранения данных
- библиотека *Telebot* для создания ботов для Telegram
- сервис *Grafana* для отображения мониторингов
- встроенная графическая библиотека *Telegram calendar* для отображения даты пользователю.
