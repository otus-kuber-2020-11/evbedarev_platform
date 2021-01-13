Домашнее задание kubernetes-operators:

	-	сделал задание  “уткой”
	
	-	сделал 2е задание *
	
Вопрос: почему объект создался, хотя мы создали CR, до того, как

запустили контроллер?

Ответ: потому что событие никто не вычитал, оно висело в очереди. При создании контроллера он вычитал и обработал.

MySQL контроллер:
	Проверяем что появились pvc:
	
	NAME                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
	
		backup-mysql-instance-pvc   Bound    pvc-f8efe37e-a7f3-4c17-8299-a57d9269af77   1Gi        RWO            standard       143m
		
		mysql-instance-pvc          Bound    pvc-f3e429e5-ac91-4365-b334-8f7bd49619bf   1Gi        RWO            standard       102m
		
	
Посмотрим содержимое таблицы:

+----+-------------+

| id | name        |

+----+-------------+

|  1 | some data   |

|  2 | some data-2 |

+----+-------------+

	Удалим mysql-instance:
	
	NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM                               STORAGECLASS   REASON   AGE
	
	backup-mysql-instance-pv                   1Gi        RWO            Retain           Available                                                               154m
	
Создадим заново mysql-instance:

+----+-------------+

| id | name        |

+----+-------------+

|  1 | some data   |

|  2 | some data-2 |

+----+-------------+
База взята из бэкапа.

Задание со 🌟 (1) пока не сделал.

Задание со 🌟 (2):

1. Смотрим текущий пароль пода (kubectl describe pod mysql-instance-75fccbd7f4-zlmxv)

    Environment:
    
      MYSQL_ROOT_PASSWORD:  otuspassword2
      
      MYSQL_DATABASE:       otus-database
      
	 Смотрим в cr.yml
	 
	 	password: otuspassword2
		
2. проверяю что база доступна с этим паролем (kubectl exec -it $MYSQLPOD -- mysql -potuspassword2 -e "select * from test;" otus-database):

+----+-------------+

| id | name        |

+----+-------------+

|  1 | some data   |

|  2 | some data-2 |

+----+-------------+

3. меняю пароль в cr.yml на otuspassword3

4. применяю. controller log:

	password changed to: otuspassword3
	
	job change-mysql-instance-job end without errors
	
	delete job: restore-mysql-instance-job
	
	job restore-mysql-instance-job end without errors
	
	old_pwd value: otuspassword2, new_pwd value: otuspassword3
	
	[2021-01-13 18:34:06,905] kopf.objects         [INFO    ] [default/mysql-instance] Handler 'change_handler' succeeded.
	
	[2021-01-13 18:34:06,906] kopf.objects         [INFO    ] [default/mysql-instance] Update event is processed: 1 succeeded; 0 failed.
	
5. смотрим что с подом:

		NAME                               READY   STATUS      RESTARTS   AGE
		
		mysql-instance-d9d5f4445-7gtt9     1/1     Running     0          55s
		
		restore-mysql-instance-job-6hk9q   0/1     Completed   3          55s
		
	Смотри что внутри пода (kubectl describe pod mysql-instance-d9d5f4445-7gtt9):
	
		Environment:
		
				MYSQL_ROOT_PASSWORD:  otuspassword3
				
				MYSQL_DATABASE:       otus-database
				
  Смотрим на под restore (kubectl describe pod restore-mysql-instance-job-6hk9q):
  
		  Command:
      /bin/sh
      
      -c
      
      mysql -u root -h mysql-instance -potuspassword3 otus-database< /backup-mysql-instance-pv/mysql-instance-dump.sql
			
6. Пытаюсь подключиться с новым паролем:

		mj@debian:~/kubernetes-operators/deploy$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword3 -e "select * from test;" otus-database
		
		mysql: [Warning] Using a password on the command line interface can be insecure.
		
		+----+-------------+
		
		| id | name        |
		
		+----+-------------+
		
		|  1 | some data   |
		
		|  2 | some data-2 |
		
		+----+-------------+
	==================================================================================================================
	Код:
	
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
						#удаляем задание и деплоймент
						api.delete_namespaced_deployment(name,'default',propagation_policy='Background')
						wait_until_job_end(f"restore-{name}-job")
						apiBatch.delete_namespaced_job(f"restore-{name}-job",'default',propagation_policy='Background')
				except kubernetes.client.rest.ApiException:
						pass
				#Инициализируем деплоймент с новым паролем
				deployment = render_template('mysql-deployment.yml.j2', {
						'name': name,
						'image': image,
						'password': password,
						'database': database})
				#Инициализируем задание с новым паролем
				restore_job = render_template('restore-job.yml.j2', {'name': name,'image': image,'password': password,'database': database})
				kopf.append_owner_reference(deployment, owner=body)
				kopf.append_owner_reference(restore_job, owner=body)
				#Создаем деплоймент и задание
				try:
						api.create_namespaced_deployment('default', deployment)
						api = kubernetes.client.BatchV1Api()
						api.create_namespaced_job('default', restore_job)
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


Шаблон change-pwd-job.yml.j2:

apiVersion: batch/v1
kind: Job
metadata:
  namespace: default
  name: change-{{ name }}-job
spec:
  template:
    metadata:
      name: change-{{ name }}-job
    spec:
      restartPolicy: OnFailure
      containers:
      - name: backup
        image: mysql:5.7
        imagePullPolicy: IfNotPresent
        command:
        - /bin/sh
        - -c
        - mysql -u root -h {{ name }} -p{{ password }} -e " UPDATE mysql.user SET authentication_string=PASSWORD('{{new_password}}') WHERE user='root';FLUSH PRIVILEGES;"  {{ database }}


	

		





	
