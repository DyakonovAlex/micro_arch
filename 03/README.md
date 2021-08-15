# Prometheus. Grafana

Это пример как инструментировать сервис в формате Prometheus

0. Проверяем состояние minikube:

```bash
$ minikube status
```

Если все хорошо, можно продолжать.

1. Собираем образ и пушем его в dockerhub:

```bash
$ sudo docker build --tag adyakonov/hello-app:latest .
$ sudo docker login
$ sudo docker push adyakonov/hello-app:latest 
```

2. Установка prometheus:

```bash
$ minikube addons disable ingress
$ kubectl create namespace monitoring
$ kubectl config set-context --current --namespace=monitoring

$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo add stable https://charts.helm.sh/stable
$ helm repo update
$ helm install prom prometheus-community/kube-prometheus-stack -f prometheus.yaml --atomic

$ helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
$ helm repo update
$ helm install nginx ingress-nginx/ingress-nginx -f nginx-ingress.yaml --atomic
```

3. Узнаем логин и пароль grafana:

```bash
$ kubectl get secret prom-grafana -o go-template='{{range $k,$v := .data}}{{"### "}}{{$k}}{{"\n"}}{{$v|base64decode}}{{"\n\n"}}{{end}}'
```

4. Прокидываем порты:

```bash
$ kubectl port-forward service/prom-grafana 9000:80
$ kubectl port-forward service/prom-kube-prometheus-stack-prometheus 9090
```

5. Установка приложения:

```bash
$ helm install myapp ./hello-chart --atomic
```

6. Проверям, что все работает:

```bash
$ curl $(minikube ip):30433/user | jq
$ curl $(minikube ip)/app/user -H "Host: hello.world" | jq
$ curl $(minikube ip):30433/metrics

$ kubectl get servicemonitor.monitoring.coreos.com
$ kubectl describe servicemonitors.monitoring.coreos.com  myapp-hello-chart
```

7. Создаем нагрузку:

```bash
$ while 1; do ab -n 50 -c 5 -H'Host: hello.world' http://192.168.99.101/app/user >> /dev/null ; sleep 3; done
```

8. Импортируем dashboard-ы в grafana