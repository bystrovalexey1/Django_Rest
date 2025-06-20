# "Сервис рассылки"

В данной работе представлен шаблон сервера или приложения со стандартнами настройками и использованием фреймворка django,
фреймворка bootstrap и стандартных его пакетов `bootstrap.min.css`,`bootstrap.min.js`. Мы разработали сервис управления рассылками BystrovNewsletters

## Зависимости проекта:
* The program uses the version Python 3.12
* amqp==5.3.1
* APScheduler==3.11.0
* asgiref==3.8.1
* billiard==4.2.1
* celery==5.5.3
* click==8.2.1
* click-didyoumean==0.3.1
* click-plugins==1.1.1
* click-repl==0.3.0
* colorama==0.4.6
* Django==5.2.1
* django-apscheduler==0.7.0
* dotenv==0.9.9
* kombu==5.5.4
* packaging==25.0
* pillow==11.2.1
* prompt_toolkit==3.0.51
* psycopg2-binary==2.9.10
* python-dateutil==2.9.0.post0
* python-dotenv==1.1.0
* six==1.17.0
* sqlparse==0.5.3
* tzdata==2025.2
* tzlocal==5.3.1
* vine==5.1.0
* wcwidth==0.2.13


## Реализованы контроллеры, для отображения домашней страницы, страниц форм: Сообщений, Получателей, Рассылок, Пользователей, страницы списка Рассылок, страницы статистики.

## Функции, которые мы будем использовать в этой версии кода:

Функционал содержится в 4-ех директориях

Директории:
1. `newsletters` - основная директория с моделями Message, Recipient, Distribution, NewslettersAttempt
2. `users` - директория для работы с пользователями
3. `config` - директория с настройками проекта
4. `static` - директория для статических файлов

`manage.py` - модуль для запуска сервера или приложения


# Инструкция по установке
[Чтобы скачать репозиторий:] (https://github.com/bystrovalexey1/CourseWork4)

Затем вам необходимо установить основные зависимости для запуска проекта в вашей системе:

```pip install -r requirements.txt```

Подождите, пока наборы данных загрузятся, это может занять некоторое время. 

## Команда проекта:

"Онлайн-школа 'Skypro'" + 
"Быстров Алексей"

## Контакт для связи с командой разработки:
"bystrovalexey15@gmail.com"

## Источники
Программа создана при поддержке онлайн-школы [skypro@skyeng.ru](https://sky.pro/#giftpopup) (С надеждои на будущее)
 ![alt текст](https://static.tildacdn.com/tild3364-3965-4237-b664-363533643431/Group_1321317003.svg)
