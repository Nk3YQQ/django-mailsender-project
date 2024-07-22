# Структура проекта
```
dfr-tracker-project/
|—— blog/ # Приложение блога
    |—— migrations/
    |—— templates/
    |—— __init__.py
    |—— admin.py
    |—— apps.py
    |—— forms.py
    |—— models.py
    |—— urls.py
    |—— views.py
|—— clients/ # Приложение клиентов
    |—— migrations/
    |—— templates/
    |—— __init__.py
    |—— admin.py
    |—— apps.py
    |—— forms.py
    |—— models.py
    |—— urls.py
    |—— views.py
|—— config/ # Настройки проекта
    |—— __init__.py
    |—— asgi.py
    |—— settings.py
    |—— urls.py
    |—— wsgi.py
|—— mailing/ # Приложение рассылок
    |—— migrations/
    |—— templates/
    |—— __init__.py
    |—— admin.py
    |—— apps.py
    |—— forms.py
    |—— models.py
    |—— urls.py
    |—— views.py
|—— main/ # Главное приложение
    |—— management/ 
    |—— templates/
    |—— templatetags/
    |—— __init__.py
    |—— apps.py
    |—— cron.py
    |—— permissions.py
    |—— services.py
    |—— urls.py
    |—— views.py
|—— media/ # Папка для изоброжений
    |—— blog/
|—— message/ # Приложение сообщений
    |—— migrations/
    |—— templates/
    |—— __init__.py
    |—— admin.py
    |—— apps.py
    |—— forms.py
    |—— models.py
    |—— urls.py
    |—— views.py
|—— users/ # Приложение пользователей
    |—— migrations/
    |—— templates/
    |—— __init__.py
    |—— admin.py
    |—— apps.py
    |—— forms.py
    |—— models.py
    |—— urls.py
    |—— views.py
|—— .dockerignore
|—— .env.sample
|—— .gitignore
|—— docker-compose.yml
|—— Dockerfile
|—— LICENSE
|—— Makefile
|—— manage.py
|—— README.md
|—— requirements.txt
```

# Результаты работы:
- ### Реализован CRUD для клиента, письма, рассылки, пользователей и блога
- ### Создан механизм для отправки уведомлений и периодических задач
- ### Разработан механизм аутентификации и авторизации
- ### Реализованы шаблоны для отображения HTML страницы
- ### Написаны тесты для приложения

# Основной стек проекта:
- ### Python 3.10
- ### Django 4.2
- ### PostgreSQL 11
- ### Django ORM
- ### Redis
- ### django-crontab
- ### Docker
- ### unittest
- ### GitHub Actions (CI)

# Как пользоваться проектом

## 1) Скопируйте проект на Ваш компьютер
```
git clone git@github.com:Nk3YQQ/django-mailsender-project.git
```

## 2) Добавьте файл .env для переменных окружения
Чтобы запустить проект, понадобятся переменные окружения, которые необходимо добавить в созданный Вами .env файл.

Пример переменных окружения необходимо взять из файла .env.sample

## 3) Запустите проект

Запуск проекта
```
make run
```

Остановка проекта
```
make stop
```
