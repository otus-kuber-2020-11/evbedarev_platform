# Домашняя работа kubernetes-gitops
- Подготовил GitLab репозиторий
- Создал helm-чарты & releases для всех микросервисов
- Собрал docker-образы для всех микросервисов
- Установил CRD helmrelease
- Установил flux в кластер
- Установил helm-operator
- Создал namespace microservices-demo с помощью flux
- Изменение Helm chart frontend на имя frontend-hipster
```bash
ts=2021-02-25T21:05:22.39263543Z caller=loop.go:236 component=sync-loop state="tag flux-sync" old=3b87c4b35e043c2043c2783b0dae9e0b33624f9e new=00705ae43afd80f252817b2220d717e8091634e9
ts=2021-02-25T21:05:23.250778371Z caller=loop.go:134 component=sync-loop event=refreshed url=ssh://git@gitlab.com/madjo1985/microservices-demo.git branch=master HEAD=00705ae43afd80f252817b2220d717e8091634e9
```
- Добавли манифесты HelmRelease всем микросервисов
- Установка Flagger
- Установка istioctl & istiod
- Создал VirtualService & Gateway
- Получил доступ к frontend через ingress
## Canary
- С canary возникли затруднения так-как флагер не поддерживает версию v1alpha3. Изменил на текущую v1beta1. Так же поменялся раздел analisys.
- Успешно установлися canary
```bash
mj@mjbian:~/Documents/kubernetes-gitops/gitlab/microservices-demo/deploy/istio$ kubectl get canary -n microservices-demo
NAME       STATUS      WEIGHT   LASTTRANSITIONTIME
frontend   Succeeded   0        2021-02-28T15:15:55Z
```
- Проверим создавшийся под
```bash
kubectl get pods -n microservices-demo -l app=frontend-primary
NAME                                READY   STATUS    RESTARTS   AGE
frontend-primary-7cc6dc5f5f-lqvh5   2/2     Running   0          5h7m
```
- Пробуем провести релиз. У меня релиз успешно установлен сразу же. Может быть из-за другой версии api.
```bash
mj@mjbian:~/Documents/kubernetes-gitops/gitlab/microservices-demo/deploy/istio$ kubectl get canary -n microservices-demo
NAME       STATUS      WEIGHT   LASTTRANSITIONTIME
frontend   Succeeded   0        2021-02-28T15:15:55Z
```
- вывод после успешной установки
```bash
j@mjbian:~/Documents/kubernetes-gitops/gitlab/microservices-demo/deploy/istio$ kubectl describe canary/frontend -n microservices-demo
Name:         frontend
Namespace:    microservices-demo
Labels:       <none>
Annotations:  <none>
API Version:  flagger.app/v1beta1
Kind:         Canary
Metadata:
  Creation Timestamp:  2021-02-28T10:51:22Z
  Generation:          1
  Managed Fields:
    API Version:  flagger.app/v1beta1
    Fields Type:  FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          .:
          f:kubectl.kubernetes.io/last-applied-configuration:
      f:spec:
        .:
        f:analysis:
          .:
          f:interval:
          f:iterations:
          f:threshold:
        f:provider:
        f:service:
          .:
          f:gateways:
          f:hosts:
          f:port:
          f:targetPort:
          f:trafficPolicy:
            .:
            f:tls:
              .:
              f:mode:
        f:targetRef:
          .:
          f:apiVersion:
          f:kind:
          f:name:
    Manager:      kubectl-client-side-apply
    Operation:    Update
    Time:         2021-02-28T10:51:22Z
    API Version:  flagger.app/v1beta1
    Fields Type:  FieldsV1
    fieldsV1:
      f:spec:
        f:service:
          f:portDiscovery:
      f:status:
        .:
        f:canaryWeight:
        f:conditions:
        f:failedChecks:
        f:iterations:
        f:lastAppliedSpec:
        f:lastTransitionTime:
        f:phase:
        f:trackedConfigs:
    Manager:         flagger
    Operation:       Update
    Time:            2021-02-28T15:15:55Z
  Resource Version:  5114651
  Self Link:         /apis/flagger.app/v1beta1/namespaces/microservices-demo/canaries/frontend
  UID:               f14ae066-2d51-45ee-b17b-94e71c1b6ea1
Spec:
  Analysis:
    Interval:    30s
    Iterations:  10
    Threshold:   10
  Provider:      istio
  Service:
    Gateways:
      frontend
    Hosts:
      *
    Port:         80
    Target Port:  8080
    Traffic Policy:
      Tls:
        Mode:  DISABLE
  Target Ref:
    API Version:  apps/v1
    Kind:         Deployment
    Name:         frontend
Status:
  Canary Weight:  0
  Conditions:
    Last Transition Time:  2021-02-28T15:15:55Z
    Last Update Time:      2021-02-28T15:15:55Z
    Message:               Canary analysis completed successfully, promotion finished.
    Reason:                Succeeded
    Status:                True
    Type:                  Promoted
  Failed Checks:           0
  Iterations:              0
  Last Applied Spec:       db6b75cd6
  Last Transition Time:    2021-02-28T15:15:55Z
  Phase:                   Succeeded
  Tracked Configs:
Events:  <none>
```
