# Основы работы с Kubernetes

Это пример минимального сервиса. Нам понадобится [minikube](https://minikube.sigs.k8s.io/docs/start/)

Сервис:

- отвечает на порту 8000
- имеет http-метод GET /health/ RESPONSE: {"status": "OK"}

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

2. Применяем манифесты k8s для этого сервиса:

```bash
$ cd ..
$ kubectl apply -f .
$ kubectl describe service/hello-service            

Name:                     hello-service
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=hello-py-app
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.106.105.151
IPs:                      10.106.105.151
Port:                     <unset>  8000/TCP
TargetPort:               web/TCP
NodePort:                 <unset>  32524/TCP
Endpoints:                172.17.0.2:80,172.17.0.4:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

На подах запущено наше приложение на порту 80 (строка Endpoints):

```bash
$ minikube ssh
$ curl 172.17.0.2:80

Hello world hello-deployment-6d5d4d8577-xgcj6!

$ exit
```

При обращении по ip к сущности service надо указывать порт 8000 (строка Port):

```bash
$ minikube ssh
$ curl 10.106.105.151:8000

Hello world hello-deployment-6d5d4d8577-xgcj6!

$ exit
```

При обращении по ip к миникубу надо указывать порт 32524 (строка NodePort):

```bash
$ curl $(minikube ip):32524

Hello world hello-deployment-6d5d4d8577-xgcj6!
```

Проверяем работу ingress: все запросы на хост arch.homework должны роутиться на сервис hello-service и \
в ingress-е должно быть правило, которое форвардит все запросы с /otusapp/adyakonov/* на сервис с rewrite-ом пути:

```bash
$ curl $(minikube ip)/otusapp/adyakonov -H "Host: arch.homework"

Hello world hello-deployment-6d5d4d8577-f8vcj!
```

Далее, мы можем добавить в /etc/hosts

```
192.168.99.101 arch.homework 
```

и тогда: 

```bash
$ curl http://arch.homework/otusapp/adyakonov/health

{'status': 'ok'}
```