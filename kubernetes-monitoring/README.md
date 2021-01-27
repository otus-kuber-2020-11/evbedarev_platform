# Домашнее задание kubernetes-monitoring:
## Dockerfile
1. Создал Dockerfile. Взял базовый  образ Centos 7 , установил nginx.
... Были проблемы с передачей переменной в конфиг nginx. Получилось решить с помощью envsubst.
## Nginx & Nginx exporter
2. Создал деплоймент с тремя контейнерами nginx, порты передаються с помощью env.
... А так же контейнер с nginx-exporter собирает метрики с порта 8081, плюс Service для nginx-exporter
... Устанавливаем деплоймент и севис.
## Prometheus
3. Клонирую репозиторий [prometheus-operator](https://github.com/prometheus-operator/kube-prometheus "prometheus-operator")
4. Устанавливаю:
```bash
kubectl create -f manifests/setup
kubectl create -f manifests/
```
5. В ServiceMonitor указываю matchLabels: nameapp: nginx-exporter.
6. с помощью kubectl port-forward лезем на localhost:9090. И наблюдаем target: node-exporter
## Grafana
График:
![grafana](‪https://downloader.disk.yandex.ru/preview/469e79419113f7906a493a3c8b863501e2128c8e6c2df0199754d16abbfa8c37/6011cb8a/UiBHz4MLSl6fxeRd7oyJrrJZfLc2Y8Kdey5s5CU0T8cW_naiG5j2FdDanhu9ufEpqL34_D6vyLDy5kAqw9jO2A%3D%3D?uid=0&filename=grafana.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2512x1324)
