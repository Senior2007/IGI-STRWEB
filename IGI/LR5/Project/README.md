# AutoParts LR5

Автомагазин запасных частей.

## Локальный запуск

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Демонстрационные пользователи:

- `admin / admin12345`
- `manager / manager12345`
- `client1 / client12345`

## Docker

```bash
docker compose up --build
```
