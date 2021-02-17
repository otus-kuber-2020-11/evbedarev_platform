# Домашняя работа kubernetes-logging
## EFK
1. Подготовка kubernetes кластера
- Создал 1 ноду default-pool и 3 ноды infra-pool
- назначил taint на ноды infa
2. Установил HipsterShop
3. Установка EFK стека | Helm charts
- установил elastic & kibana & fluent-bit
- добавил tolerations в elasticsearch.values.yaml
```yaml
tolerations:
  - key: node-role
    operator: Equal
    value: infra
    effect: NoSchedule
```
- добавил nodeSelector в elasticsearch.values.yaml
```yaml
nodeSelector:
  cloud.google.com/gke-nodepool: infra-pool
```
получилось: 
```bash
mj@mjbian:~/Documents/kubernetes-logging$ kubectl get pods -n logging -o wide -n observability
NAME                     READY   STATUS    RESTARTS   AGE    IP         NODE                                     NOMINATED NODE   READINESS GATES
elasticsearch-master-0   1/1     Running   0          2m6s   10.4.2.2   gke-cluster-1-infra-pool-e11f6aff-bj1r   <none>           <none>
elasticsearch-master-1   1/1     Running   0          2m6s   10.4.0.2   gke-cluster-1-infra-pool-e11f6aff-vw7w   <none>           <none>
elasticsearch-master-2   1/1     Running   0          2m6s   10.4.1.7   gke-cluster-1-infra-pool-e11f6aff-585g   <none>           <none>
```
4. Установка nginx-ingress
- Неточность в приложеном values.yaml. Вместо метки "app" надо использовать "app.kubernetes.io/name"
- после установки получилось это:
```bash
NAME                                        READY   STATUS    RESTARTS   AGE     IP         NODE                                     NOMINATED NODE   READINESS GATES
ingress-nginx-controller-64f4d48fdd-5h75n   1/1     Running   0          6m44s   10.4.0.8   gke-cluster-1-infra-pool-e11f6aff-vw7w   <none>           <none>
ingress-nginx-controller-64f4d48fdd-978rs   1/1     Running   0          6m44s   10.4.1.8   gke-cluster-1-infra-pool-e11f6aff-585g   <none>           <none>
ingress-nginx-controller-64f4d48fdd-cmn5z   1/1     Running   0          6m44s   10.4.2.7   gke-cluster-1-infra-pool-e11f6aff-bj1r   <none>           <none>
```
5. УстановкаEFKстека |Kibana
- сделал установку helm-chart-kibana с kibana.values.yaml
```bash
mj@mjbian:~/Documents/kubernetes-logging$ kubectl get Ingress -n observability
NAME                 HOSTS                         ADDRESS       PORTS   AGE
kibana-kibana        kibana.35.202.86.5x.xip.io    35.188.0.8   80      82s

```
6. Настройка FluenBit
- применил fluent-bit.values.yaml
- исправил проблему с time & timestamp с помощью фильтра.
- добавил в fluent-bit.values.yaml [INPUT] & tolerations(что бы установка происходила и на ноды infa)
7. Установил node-exporter
8. Провери что метрики действительно собираются корректно.
9. Добился что логи появились(в fluentbit добавил tolerations & [Input] секцию)
10. Добавил в ingress.values.yaml:
```yaml
controller:
  config:
    log-format-escape-json: true
    log-format-upstream: '{"time": "$time_iso8601", "remote_addr": "$proxy_protocol_addr", "x_forward_for": "$proxy_add_x_forwarded_for", "request_id": "$req_id",
  "remote_user": "$remote_user", "bytes_sent": $bytes_sent, "request_time": $request_time, "responseStatus": $status, "vhost": "$host", "request_proto": "$server_protocol",
  "path": "$uri", "request_query": "$args", "request_length": $request_length, "duration": $request_time,"method": "$request_method", "http_referrer": "$http_referer",
  "http_user_agent": "$http_user_agent" }'
```
11. Создал 3 дашборда в kibana

## Loki
12. Установил Loki & promtail
13. Добавил в конфигурацию prometheus-operator.values.yaml:
```yaml
  additionalDataSources:
   - name: loki
     type: loki
     url: http://loki.observability.svc.cluster.local:3100/
```
14. Пришлось создать promtail.values.yaml потому что он не отправлял метрики со стандартными параметрами
15. Настроил дашборд для nginx-ingress
