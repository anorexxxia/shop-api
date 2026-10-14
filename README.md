# ShopAPI

REST API интернет-магазина бытовой техники на FastAPI с PostgreSQL, Nginx и отдельным gRPC-сервисом авторизации.

## Архитектура

- **FastAPI** — REST API для работы с клиентами, товарами, поставщиками и изображениями.
- **Auth Service** — отдельный сервис авторизации на gRPC, выдающий JWT.
- **PostgreSQL** — хранение данных магазина и авторизации.
- **Nginx** — reverse proxy, балансировка запросов, HTTPS, раздача статики и кэширование запросов к pgAdmin.
- **pgAdmin** — веб-интерфейс для управления PostgreSQL.
- **Docker Compose** — запуск и взаимодействие сервисов.

## Требования

- Git
- Docker Engine и Docker Compose
- OpenSSL для создания локального HTTPS-сертификата

## 1. Клонирование репозитория

```bash
git clone https://github.com/anorexxxia/shop-api.git
cd shop-api
```

## 2. Настройка переменных окружения

Перед запуском создайте локальные файлы конфигурации на основе шаблонов:

```bash
cp .env.example.postgres .env.postgres
cp .env.example .env.main
cp .env.example.readonly .env.readonly
cp .env.example.pgadmin .env.pgadmin
cp .env.example.auth .env.auth
```

Перед запуском отредактируйте созданные файлы.

### `.env.postgres`

Содержит настройки PostgreSQL:

- `POSTGRES_USER` и `POSTGRES_PASSWORD` — пользователь-владелец основной базы данных и его пароль.
- `POSTGRES_DB` — имя основной базы магазина, например `shop_api`.
- `READONLY_DB_USER` и `READONLY_DB_PASSWORD` — учётные данные пользователя с доступом только на чтение.

### `.env.main`

Настройки основного экземпляра REST API. Укажите те же `DB_USER` и `DB_PASSWORD`, что и в `.env.postgres`, а также `DB_NAME`, совпадающий с `POSTGRES_DB`.

- `DB_HOST=postgres`
- `DB_PORT=5432`
- `MAIN_INSTANCE=true`
- `AUTH_HOST=auth`
- `AUTH_PORT=50051`

### `.env.readonly`

Настройки экземпляров REST API для чтения. Значения `DB_USER` и `DB_PASSWORD` должны совпадать с `READONLY_DB_USER` и `READONLY_DB_PASSWORD` из `.env.postgres`.

- `DB_HOST=postgres`
- `DB_PORT=5432`
- `DB_NAME` должен совпадать с `POSTGRES_DB`.
- `MAIN_INSTANCE=false`
- `AUTH_HOST=auth`
- `AUTH_PORT=50051`

### `.env.auth`

Настройки gRPC-сервиса авторизации.

- `DB_HOST=postgres`
- `DB_PORT=5432`
- `DB_NAME=grpc_auth`
- `DB_USER` и `DB_PASSWORD` — учётные данные владельца базы, указанные в `.env.postgres`.
- `SECRET_KEY` — уникальный случайный секрет для подписи JWT.

Для генерации секрета можно использовать Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### `.env.pgadmin`

Содержит `PGADMIN_DEFAULT_EMAIL` и `PGADMIN_DEFAULT_PASSWORD` — данные для входа в веб-интерфейс pgAdmin.

## 3. Настройка HTTPS

Nginx использует сертификат и приватный ключ из каталога `certs/`:

- `certs/shop.crt` — SSL-сертификат;
- `certs/shop.key` — приватный ключ.

Эти файлы не хранятся в Git. При первом запуске на новом компьютере необходимо создать каталог и самоподписанный сертификат.

```bash
mkdir -p certs

openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout certs/shop.key \
  -out certs/shop.crt \
  -subj "/CN=shop" \
  -addext "subjectAltName=DNS:shop"

chmod 600 certs/shop.key
```

Самоподписанный сертификат предназначен для локальной разработки. Браузер может предупреждать о недоверенном сертификате.

## 4. Настройка имени `shop` в Windows

Чтобы открывать проект по адресу `https://shop`, необходимо связать имя `shop` с IP-адресом компьютера, на котором работает Nginx.

1. Откройте Блокнот от имени администратора.
2. Откройте файл:

   ```text
   C:\Windows\System32\drivers\etc\hosts
   ```

3. Добавьте строку:

   ```text
   127.0.0.1 shop
   ```

4. Сохраните файл.

Этот вариант подходит, если Docker работает на том же компьютере. Если проект запущен на другом компьютере в локальной сети, вместо `127.0.0.1` укажите IP-адрес этого компьютера.

После запуска проекта сайт будет доступен по адресу:

- `https://shop/` — главная страница.

## 5. Запуск проекта

После настройки переменных окружения и создания HTTPS-сертификата выполните из корневого каталога проекта:

```bash
docker compose up --build -d
```
Проверить состояние контейнеров:

```bash
docker compose ps
```

Посмотреть логи всех сервисов:

```bash
docker compose logs
```

Посмотреть логи конкретного сервиса, например Auth Service:

```bash
docker compose logs auth
```

Чтобы остановить сервисы:

```bash
docker compose down
```

## 6. Доступные адреса

После успешного запуска сервисы доступны по следующим адресам:

| Сервис | Адрес | Назначение |
|---|---|---|
| Главная страница | `https://shop/` | Статический сайт |
| REST API | `https://shop/api/v1/` | API интернет-магазина |
| Swagger UI | `https://shop/api/v1` | Документация REST API |
| OpenAPI | `https://shop/openapi.json` | Схема API |
| Nginx Status | `https://shop/status` | Статистика Nginx |
| pgAdmin | `https://shop/admin/` | Управление PostgreSQL |

Для локального доступа по имени `shop` предварительно настройте файл `hosts` в Windows.

## 7. Балансировка запросов

Nginx распределяет GET-запросы между тремя экземплярами REST API:

- `api-main` — вес 2;
- `api-read1` — вес 1;
- `api-read2` — вес 1.

Запросы, отличные от GET, направляются только в `api-main`.

Таким образом, основной экземпляр обслуживает операции записи, а остальные экземпляры используются для распределения запросов на чтение.

## 8. Базы данных

PostgreSQL использует две базы данных:

- `shop_api` — данные интернет-магазина;
- `grpc_auth` — данные сервиса авторизации.

Скрипт `postgres/init.sh` создаёт базу авторизации и пользователя с доступом только на чтение к основной базе магазина.

Скрипты инициализации PostgreSQL выполняются автоматически только при первом запуске с пустым каталогом данных. Изменение скрипта после создания базы не приводит к его повторному выполнению.

## Технологии

- Python
- FastAPI
- gRPC и Protocol Buffers
- SQLAlchemy и asyncpg
- PostgreSQL
- Nginx
- Docker Compose
- JWT
- pytest
