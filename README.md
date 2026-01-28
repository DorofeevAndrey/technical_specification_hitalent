## API-сервис для вопросов и ответов (FastAPI + PostgreSQL)

### Описание
REST API для вопросов и ответов:
- **Question**: `id`, `text`, `created_at`
- **Answer**: `id`, `question_id`, `user_id`, `text`, `created_at`

Стек:
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy ORM**
- **Alembic миграции**

Swagger UI: `http://localhost:8000/docs`

---

### Запуск через Docker (рекомендуется)

Требования:
- Docker
- Docker Compose

Запуск:

```bash
docker compose up --build
```

Если ранее поднимал Postgres другой версии и словил ошибку несовместимости data directory — сбрось volume:

```bash
docker compose down -v
docker compose up --build
```

После запуска:
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

---

### Эндпоинты

#### Questions
- `GET /questions/` — список всех вопросов
- `POST /questions/` — создать новый вопрос
- `GET /questions/{id}` — получить вопрос и все ответы на него
- `DELETE /questions/{id}` — удалить вопрос (вместе с ответами)

#### Answers
- `POST /questions/{id}/answers/` — добавить ответ к вопросу
- `GET /answers/{id}` — получить конкретный ответ
- `DELETE /answers/{id}` — удалить ответ

---

### Примеры запросов

Создать вопрос:

```bash
curl -X POST "http://localhost:8000/questions/" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Как устроены миграции Alembic?\"}"
```

Добавить ответ к вопросу:

```bash
curl -X POST "http://localhost:8000/questions/1/answers/" ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":\"user-123\",\"text\":\"Через alembic revision и alembic upgrade head\"}"
```

Получить вопрос со всеми ответами:

```bash
curl "http://localhost:8000/questions/1"
```

Удалить вопрос (ответы удалятся каскадно):

```bash
curl -X DELETE "http://localhost:8000/questions/1"
```

---

### Бизнес-логика
- Нельзя создать ответ к несуществующему вопросу (вернётся `404`).
- Один и тот же пользователь может оставлять несколько ответов на один вопрос (уникальных ограничений нет).
- При удалении вопроса ответы удаляются каскадно (`ON DELETE CASCADE`).

---

### Миграции
Миграции управляются Alembic (папка `migrations/`).

В Docker сервис `web` перед запуском приложения выполняет:
- `alembic upgrade head`

---

### Переменные окружения
Приложение использует:
- `DB_USER` (по умолчанию `postgres`)
- `DB_PASS` (по умолчанию `postgres`)
- `DB_HOST` (в Docker должен быть `db`)
- `DB_PORT` (по умолчанию `5432`)
- `DB_NAME` (по умолчанию `hitalent`)

---

### Структура проекта (кратко)
- `app/models/` — ORM-модели SQLAlchemy
- `app/schemas/` — Pydantic-схемы
- `app/api/v1/routes/` — роуты FastAPI
- `migrations/` — Alembic миграции

### Тестирование

Проект использует pytest для модульного и интеграционного тестирования.

#### Запуск тестов

**С помощью Docker:**
```bash
docker compose exec web python -m pytest