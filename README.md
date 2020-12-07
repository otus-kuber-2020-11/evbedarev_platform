# evbedarev_platform
evbedarev Platform repository
Разберитесь почему все pod в namespace kube-system
восстановились после удаления:
- Потому что эти поды запущены как статические, которые управляются kubelet локально на ноде.
- coredns потому что установлена replica set

Что делал:
создал Dockertfile, контейнер и запушил его в dockerhub madjo/kuber:apache
создал под web, init container, примонтировал раздел /app. Запустил и проверил доступность страницы.
Нашел проблему в том что не хватало переменных в манифесте.
