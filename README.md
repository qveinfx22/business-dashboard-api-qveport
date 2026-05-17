# backend for business dashboard

Небольшой backend на `FastAPI`.

Что внутри:

- авторизация по JWT
- PostgreSQL
- CRUD для товаров
- CRUD для заказов
- простая админка на `sqladmin`

## запуск

```powershell
pip install -r requirements.txt
```

Поднять базу:

```powershell
docker compose up -d
```

Потом создать `.env` на основе `.env.example` и запустить сервер:

```powershell
uvicorn app.main:app --reload
```

## основные роуты

- `POST /api/auth/login`
- `GET /api/users`
- `POST /api/users`
- `GET /api/products`
- `POST /api/products`
- `PUT /api/products/{product_id}`
- `DELETE /api/products/{product_id}`
- `GET /api/orders`
- `POST /api/orders`
- `PUT /api/orders/{order_id}`
- `DELETE /api/orders/{order_id}`

## админка

`http://127.0.0.1:8000/admin`

Первый админ создается при старте приложения из значений в `.env`.
