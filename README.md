# Microservice Architecture

## 01. Основы работы с Kubernetes

Пример минимального сервиса.

Сервис:

- отвечает на порту 8000
- имеет http-метод GET /health/ RESPONSE: {"status": "OK"}

Манифесты описывают сущности Deployment, Service, Ingress. Хост в ингрессе arch.homework. В Ingress-е есть правило, которое форвардит все запросы
