# 📚 FastAPI Бэкенд сайта библиотеки


FastAPI-приложение для управления библиотекой. Поддерживает регистрацию пользователей, управление книгами и авторами, а также систему бронирования книг.


## Основные возможности
- Регистрация и авторизация — реализована с помощью FastAPI Users.
- CRUD для книг и авторов — добавление, обновление, удаление и просмотр информации о книгах и авторах.
- Одалживание книг — возможность бронирования книг.


## Установка и запуск


```bash
git clone https://github.com/Relanit/fastapi_rest.git
cd fastapi_rest
docker build . -t fastapi_rest:latest
docker compose build
docker compose up -d
```

Документация API будет доступна по адресу: http://localhost:9999/docs

Примечание: при логине через документацию, в поле "username" нужно вводить email, указанный при регистрации:
![Логин](assets/login.png)

## Запуск тестов
```bash
docker compose --env-file .env.test exec app pytest -v -s
```




