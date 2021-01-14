import kopf
import yaml
import kubernetes
import time
from jinja2 import Environment, FileSystemLoader

def wait_until_job_end(jobname):
    api = kubernetes.client.BatchV1Api()
    job_finished = False
    jobs = api.list_namespaced_job('default')
    while (not job_finished) and any(job.metadata.name == jobname for job in jobs.items):
        time.sleep(1)
        jobs = api.list_namespaced_job('default')
        for job in jobs.items:
            if job.metadata.name == jobname:
                if job.status.succeeded == 1:
                    job_finished = True
                    print(f"job {jobname} end without errors")

def render_template(filename, vars_dict):
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template(filename)
    yaml_manifest = template.render(vars_dict)
    json_manifest = yaml.load(yaml_manifest)
    return json_manifest

def delete_success_jobs(mysql_instance_name):
    print("Begin deletion success jobs")
    api = kubernetes.client.BatchV1Api()
    jobs = api.list_namespaced_job('default')
    for job in jobs.items:
        jobname = job.metadata.name
        print(f"get jobname: {jobname}")
        if (jobname == f"backup-{mysql_instance_name}-job") or \
                (jobname == f"restore-{mysql_instance_name}-job"):
            if job.status.succeeded == 1:
                api.delete_namespaced_job(jobname,'default',propagation_policy='Background')
                print(f"{jobname} succeeded and will be deleted")
    print("End deletion success jobs")

#меняет пароль от текущей базы
def change_curr_pwd(name, password, new_password, database):
    print(f"get name: {name}")
    #инициализация задания из шаблона, передача параметров
    change_pwd = render_template('change-pwd-job.yml.j2', {'name': name,'password': password,'new_password': new_password,'database': database})
    api = kubernetes.client.BatchV1Api()
    try:
        #Создаем задание на изменеие пароля
        api.create_namespaced_job('default', change_pwd)
    except kubernetes.client.rest.ApiException:
        pass
    print(f"password changed to: {new_password}")
    #Ожидаем пока задание выполниться
    wait_until_job_end(f"change-{name}-job")
    try:
        #Удаляем задание на изменение
        api.delete_namespaced_job(f"change-{name}-job",'default',propagation_policy='Background')
    except kubernetes.client.rest.ApiException:
        pass

#функция на обновление ресурсов с новым паролем(deployment, restore_job)
def update_res(name, image, password, database, body):
    api = kubernetes.client.AppsV1Api()
    apiBatch = kubernetes.client.BatchV1Api()
    print(f"delete job: restore-{name}-job")
    try:
        #удаляем деплоймент
        api.delete_namespaced_deployment(name,'default',propagation_policy='Background')
        wait_until_job_end(f"restore-{name}-job")
    except kubernetes.client.rest.ApiException:
        pass
    #Инициализируем деплоймент с новым паролем
    deployment = render_template('mysql-deployment.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})
    kopf.append_owner_reference(deployment, owner=body)
    #Создаем деплоймент и задание
    try:
        api.create_namespaced_deployment('default', deployment)
        api = kubernetes.client.BatchV1Api()
    except kubernetes.client.rest.ApiException:
        pass

#Запускем функцию change_handler при наступлении события update
@kopf.on.update('otus.homework', 'v1', 'mysqls')
def change_handler(body, old, new, diff, **_):
    old_password = old['spec']['password']
    new_password = new['spec']['password']
    #если старый пароль отличается от нового то начинаем
    if (old_password != new_password):
        name = body['metadata']['name']
        image = body['spec']['image']
        database = body['spec']['database']

        change_curr_pwd(name, old_password, new_password, database)
        update_res(name, image, new_password, database, body)
        print(f"old_pwd value: {old_password}, new_pwd value: {new_password}")    


@kopf.on.create('otus.homework', 'v1', 'mysqls')
# Функция, которая будет запускаться при создании объектов тип MySQL:
def mysql_on_create(body, spec,**_):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    database = body['spec']['database']
    storage_size = body['spec']['storage_size']

    # Генерируем JSON манифесты для деплоя
    persistent_volume = render_template('mysql-pv.yml.j2',
                                        {'name': name,
                                         'storage_size': storage_size})
    persistent_volume_claim = render_template('mysql-pvc.yml.j2',
                                              {'name': name,
                                               'storage_size': storage_size})
    service = render_template('mysql-service.yml.j2', {'name': name})

    deployment = render_template('mysql-deployment.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})
    restore_job = render_template('restore-job.yml.j2', {'name': name,'image': image,'password': password,'database': database})

    kopf.append_owner_reference(persistent_volume, owner=body)
    kopf.append_owner_reference(persistent_volume_claim, owner=body) # addopt
    kopf.append_owner_reference(service, owner=body)
    kopf.append_owner_reference(deployment, owner=body)
    kopf.append_owner_reference(restore_job, owner=body)
    api = kubernetes.client.CoreV1Api()
    # Создаем mysql PV:
    api.create_persistent_volume(persistent_volume)
    # Создаем mysql PVC:
    api.create_namespaced_persistent_volume_claim('default', persistent_volume_claim)
    # Создаем mysql SVC:
    api.create_namespaced_service('default', service)

    # Создаем mysql Deployment:
    api = kubernetes.client.AppsV1Api()
    api.create_namespaced_deployment('default', deployment)
    try:
        api = kubernetes.client.BatchV1Api()
        api.create_namespaced_job('default', restore_job)
        wait_until_job_end(f"restore-{name}-job")
        api.delete_namespaced_job(f"restore-{name}-job",'default',propagation_policy='Background')
    except kubernetes.client.rest.ApiException:
        pass
    try:
        backup_pv = render_template('backup-pv.yml.j2', {'name': name})
        api = kubernetes.client.CoreV1Api()
        api.create_persistent_volume(backup_pv)
        message = "Without restore job"
    except kubernetes.client.rest.ApiException:
        pass
    if 'message' not in locals():
        message = "With restore job"
    try:
        backup_pvc = render_template('backup-pvc.yml.j2', {'name': name})
        api = kubernetes.client.CoreV1Api()
        api.create_namespaced_persistent_volume_claim('default', backup_pvc)
    except kubernetes.client.rest.ApiException:
        pass
    return {'message': message}

@kopf.on.delete('otus.homework', 'v1', 'mysqls')
def delete_object_make_backup(body, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    database = body['spec']['database']
    # Cоздаем backup job:
    
    api = kubernetes.client.BatchV1Api()
    backup_job = render_template('backup-job.yml.j2', {'name': name,'image': image,'password': password,'database': database})
    api.create_namespaced_job('default', backup_job)
    wait_until_job_end(f"backup-{name}-job")
    delete_success_jobs(name)
    return {'message': "mysql and its children resources deleted"}

