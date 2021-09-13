# Microservice Architecture

## 01. Основы работы с Kubernetes

Пример минимального сервиса.

Сервис:

- отвечает на порту 8000
- имеет http-метод GET /health/ RESPONSE: {"status": "OK"}

Манифесты описывают сущности Deployment, Service, Ingress. Хост в ингрессе arch.homework. В Ingress-е есть правило, которое форвардит все запросы

## 02. Основы работы с Kubernetes

Пример простейшего RESTful CRUD.

- БД Postgresql
- Инициализация БД
  - создание таблицы data
  - вставка 1 записи

Сервис:

- отвечает на порту 8000
- имеет следущие http-методы 
  - GET /user - получить всех пользователей
  - GET /user/{{userId}} - получить конкретного пользователя
  - POST /user - создание пользователя
  - PUT /user/{{userId}} - обновить пользователя
  - DELETE /user/{{userId}} - удалить пользователя

Пример body для создания пользователя:

```json
{
    "name": "test",
    "email": "test@gmail.com",
    "phone": 54321
}
```

Приложена Postman коллекция, в которой представлены примеры запросов к сервису на создание, получение, изменение и удаление пользователя.

## 03. Prometheus, Grafana

Пример как инструментировать сервис метриками в формате Prometheus

## 04. Service mesh Istio

## 05. Apigateway
