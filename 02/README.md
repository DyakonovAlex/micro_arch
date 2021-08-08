# Основы работы с Kubernetes

Это пример простейшего RESTful CRUD. Нам понадобится [minikube](https://minikube.sigs.k8s.io/docs/start/)

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

0. Проверяем состояние minikube:

```bash
$ minikube status
```

Если все хорошо, можно продолжать.

1. Собираем образ и пушем его в dockerhub:

```bash
$ cd hello-py/
$ sudo docker build --tag adyakonov/hello-app:latest .
$ sudo docker login
$ sudo docker push adyakonov/hello-app:latest 
```

2. Установка приложения:

```bash
$ cd ..
$ helm install myapp ./hello-chart
```

Проверяем работу ingress: все запросы на хост arch.homework должны роутиться на сервис hello-service и \
в ingress-е должно быть правило, которое форвардит все запросы с /otusapp/adyakonov/* на сервис с rewrite-ом пути:

```bash
$ curl $(minikube ip)/otusapp/adyakonov/user -H "Host: arch.homework" | jq

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    64  100    64    0     0  10666      0 --:--:-- --:--:-- --:--:-- 10666
[
  {
    "email": "vasya@ya.ru",
    "id": 1,
    "name": "vasya",
    "phone": "12345"
  }
]
```

Далее, мы можем добавить в /etc/hosts

```bash
192.168.99.101 arch.homework 
```

и тогда: 

```bash
$  curl http://arch.homework/otusapp/adyakonov/user | jq

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    64  100    64    0     0  16000      0 --:--:-- --:--:-- --:--:-- 16000
[
  {
    "email": "vasya@ya.ru",
    "id": 1,
    "name": "vasya",
    "phone": "12345"
  }
]
```