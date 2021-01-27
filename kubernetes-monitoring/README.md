# Домашнее задание kubernetes-monitoring:
## Dockerfile
1. Создал Dockerfile. Взял базовый  образ Centos 7 , установил nginx.
... Были проблемы с передачей переменной в конфиг nginx. Получилось решить с помощью envsubst.
## Nginx & Nginx exporter
2. Создал деплоймент с тремя контейнерами nginx, порты передаються с помощью env.
... А так же контейнер с nginx-exporter собирает метрики с порта 8081, плюс Service для nginx-exporter
... Устанавливаем деплоймент и севис.
## Prometheus
3. Клонирую репозиторий [prometheus-operator][1]
[1]: https://github.com/prometheus-operator/kube-prometheus
4. Устанавливаю:
```bash
kubectl create -f manifests/setup
kubectl create -f manifests/
```
5. В ServiceMonitor указываю matchLabels: nameapp: nginx-exporter.
6. с помощью kubectl port-forward лезем на localhost:9090. И наблюдаем target: node-exporter
