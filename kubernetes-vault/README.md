- Дз Kubernetes vault. Без звездочек.

- Вывод статус подов
```bash
mj@mjbian:~$ helm status vault
NAME: vault
LAST DEPLOYED: Sun Mar 14 13:18:13 2021
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
```


- Распечатаем каждый под
```bash
kubectl exec -it vault-0 -- vault operator unseal

Unseal Key (will be hidden):
Key                    Value
---                    -----
Seal Type              shamir
Initialized            true
Sealed                 false
Total Shares           1
Threshold              1
Version                1.6.2
Storage Type           consul
Cluster Name           vault-cluster-03bd0ceb
Cluster ID             cbcd6fb8-bb10-0503-5317-862cb4e5cfc4
HA Enabled             true
HA Cluster             https://vault-0.vault-internal:8201
HA Mode                standby
Active Node Address    http://10.4.2.5:8200

kubectl exec -it vault-1 -- vault operator unseal

Unseal Key (will be hidden):
Key                    Value
---                    -----
Seal Type              shamir
Initialized            true
Sealed                 false
Total Shares           1
Threshold              1
Version                1.6.2
Storage Type           consul
Cluster Name           vault-cluster-03bd0ceb
Cluster ID             cbcd6fb8-bb10-0503-5317-862cb4e5cfc4
HA Enabled             true
HA Cluster             https://vault-0.vault-internal:8201
HA Mode                standby
Active Node Address    http://10.4.2.5:8200


kubectl exec -it vault-2 -- vault operator unseal

Unseal Key (will be hidden):
Key                    Value
---                    -----
Seal Type              shamir
Initialized            true
Sealed                 false
Total Shares           1
Threshold              1
Version                1.6.2
Storage Type           consul
Cluster Name           vault-cluster-03bd0ceb
Cluster ID             cbcd6fb8-bb10-0503-5317-862cb4e5cfc4
HA Enabled             true
HA Cluster             https://vault-0.vault-internal:8201
HA Mode                standby
Active Node Address    http://10.4.2.5:8200
```
- Вывод после логина:
```bash
kubectl exec -ti vault-0 -- vault login

Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                s.OoL7wNxGg6Km0cljJFBnLvkV
token_accessor       NTH7uoIGVTH2brvtgPgkpxWr
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```

- Запрос списка авторизации
```bash
kubectl exec -ti vault-0 -- vault auth list

Path      Type     Accessor               Description
----      ----     --------               -----------
token/    token    auth_token_beabc3e7    token based credentials
```

- Вывод команды чтения секрета
```bash
kubectl exec -ti vault-0 -- vault kv get otus/otus-rw/config

====== Data ======
Key         Value
---         -----
password    asajkjkahs 
username    otus
```
- Ошибки при записи
* Не работает потому, что в правилах  стоят разрешение на чтение, создание, отображение. В конфиге надо добавить update.


- Выдача при создании сертификата
```bash
Key                 Value
---                 -----
ca_chain            [-----BEGIN CERTIFICATE-----
MIIDnDCCAoSgAwIBAgIUH1j9i/44bZ2d+CExIHGIf4OEqtEwDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhhbXBsZS5ydTAeFw0yMTAzMjIyMTI5MDVaFw0yNjAz
MjEyMTI5MzVaMCwxKjAoBgNVBAMTIWV4YW1wbGUucnUgSW50ZXJtZWRpYXRlIEF1
dGhvcml0eTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOnb752b8P1y
WaIO4ZT1a9SBJZtImy1odzIP+w4KeUdyNtzipVwqLcRq5oP6td54YiY76w+sd6Ta
xR0BUBo3ItL2RPH3hWeAT3Ay0wzmXuGoZeLPmmLuxAWzOiyR8M/2iPaJnZ3Gmsgr
Xt+PDqTyNaQ1YX5JZqitaT4M19bq8wi9Or/XqLlPwBqFy9D5/5cotHylOF1qp6XW
k7gsqwt6dunn+SH55xSLPocOPYw1OfAC6BC8A2sVF4pECXTtFXwGDUritaIPtbvL
gcjv0pPzFqWglTWBmtGHB3ngAtoG/Kt7a7eH5KuvnqyILwCXta9xoCop3FK/Fjsr
XSItNDjETpUCAwEAAaOBzDCByTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUw
AwEB/zAdBgNVHQ4EFgQU5LfQIgxlD9PEMTV0HBHZYsnzAucwHwYDVR0jBBgwFoAU
jIbzqaEhOhLQuVkUXx/oYXTBN+YwNwYIKwYBBQUHAQEEKzApMCcGCCsGAQUFBzAC
hhtodHRwOi8vdmF1bHQ6ODIwMC92MS9wa2kvY2EwLQYDVR0fBCYwJDAioCCgHoYc
aHR0cDovL3ZhdWx0OjgyMDAvdjEvcGtpL2NybDANBgkqhkiG9w0BAQsFAAOCAQEA
IBViCba7Vfy5e5xzL+yI7Vseahc0KVIdMlCVOG2J6lcC2KpcJ9tdpbyQ6/WY6YDD
jNrPMs+a72qXbCmuFWYCVM5nVhwKvFL7jbopd06AGGmweyH97jXGtDAv6TUpkqRA
MZawrx4B7YTjpKzoAben0UP233/K5zR+WeIWysh/9hAESysR/wwxX/IGJj6nmqSp
gv8ybNobXAe1hAfDWQgRJ6bYbawJ0cTcrgEDT1QQyYm3ay1IsWkf6NW4EDQxJG0i
Y90hRKwk4cy8n7QKELOGLqKnUzcxzNMjcpJ8BfE1P6Nq2uL1m2AWJXeMI3hF2S5W
5PxnwmkvBTJVaSikGvoY4Q==
-----END CERTIFICATE-----]
certificate         -----BEGIN CERTIFICATE-----
MIIDZTCCAk2gAwIBAgIUWYXBG8SRIuKuAgBHM/8M9TGKBDkwDQYJKoZIhvcNAQEL
BQAwLDEqMCgGA1UEAxMhZXhhbXBsZS5ydSBJbnRlcm1lZGlhdGUgQXV0aG9yaXR5
MB4XDTIxMDMyMjIxMzY1N1oXDTIxMDMyMzIxMzcyN1owGzEZMBcGA1UEAxMQZ2l0
bGFiLmRldmxhYi5ydTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAK0t
j3+4jjlPoWJf+sVPfzdmMVYIy0A/0BS8TCw/ZH3817bc3QikqacyZmhgxy5yJdfJ
ihUbgXqwKgCDHCUGFCPSDPExgQOTyMAmDp7HC7H9czLvzuix6IkSplI29IegBb5g
/lI5DIe2OZL7NfFUtZ4UhlFcPQl1fQCw+T/hf+eS33F2hiRMFjwM48AOTke7KY5A
nhh10QSY6lugrdTooaMK8Z9NeZEtJrWf4FsMV7xurGgu0YX5fLVxkxrKBTSdKPtO
NFqdKzkvnvkOhjpyB0CliBYRjPL2TJVit25hGoUR2TuLN11g4K0jbCzkYg+slU+y
enWpbK2gAJto3toCSJECAwEAAaOBjzCBjDAOBgNVHQ8BAf8EBAMCA6gwHQYDVR0l
BBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMB0GA1UdDgQWBBTcqFbGzKgHn62De5Vp
JkqJRdX15TAfBgNVHSMEGDAWgBTkt9AiDGUP08QxNXQcEdliyfMC5zAbBgNVHREE
FDASghBnaXRsYWIuZGV2bGFiLnJ1MA0GCSqGSIb3DQEBCwUAA4IBAQBFhIRpDxY0
Wpq4dW+rNXi5GPzG5nIevmx59YwzjqOdV9JomdzIiuW3g/D2xZ7BKhAXvvUvU6Yd
OSzFxVCfOHhI6V39IljSlnPwxQhrr5mCAKofzrUb+A1L5CsSg8jY2/5k+lIDnxYT
b/MBBEXPX/iFOZqjffhTYB1Dkvfrx44zzTuwQoCH4Yz7DN9FovqEYotKOvSN2CJ4
f+XKP7bCUpdWGH+NGpuB6AXGxUY/xB2T1Zq7+dznmZrXW6gM7d/PmsSoMT/UN10H
N62IlXEH8JzC8yxWKLDFDk62clDPQ+i5/dBM3w5GkGykE6h8fX6BBgm+1TDAm1l0
Nmc5ZPuPmhLH
-----END CERTIFICATE-----
expiration          1616535447
issuing_ca          -----BEGIN CERTIFICATE-----
MIIDnDCCAoSgAwIBAgIUH1j9i/44bZ2d+CExIHGIf4OEqtEwDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhhbXBsZS5ydTAeFw0yMTAzMjIyMTI5MDVaFw0yNjAz
MjEyMTI5MzVaMCwxKjAoBgNVBAMTIWV4YW1wbGUucnUgSW50ZXJtZWRpYXRlIEF1
dGhvcml0eTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOnb752b8P1y
WaIO4ZT1a9SBJZtImy1odzIP+w4KeUdyNtzipVwqLcRq5oP6td54YiY76w+sd6Ta
xR0BUBo3ItL2RPH3hWeAT3Ay0wzmXuGoZeLPmmLuxAWzOiyR8M/2iPaJnZ3Gmsgr
Xt+PDqTyNaQ1YX5JZqitaT4M19bq8wi9Or/XqLlPwBqFy9D5/5cotHylOF1qp6XW
k7gsqwt6dunn+SH55xSLPocOPYw1OfAC6BC8A2sVF4pECXTtFXwGDUritaIPtbvL
gcjv0pPzFqWglTWBmtGHB3ngAtoG/Kt7a7eH5KuvnqyILwCXta9xoCop3FK/Fjsr
XSItNDjETpUCAwEAAaOBzDCByTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUw
AwEB/zAdBgNVHQ4EFgQU5LfQIgxlD9PEMTV0HBHZYsnzAucwHwYDVR0jBBgwFoAU
jIbzqaEhOhLQuVkUXx/oYXTBN+YwNwYIKwYBBQUHAQEEKzApMCcGCCsGAQUFBzAC
hhtodHRwOi8vdmF1bHQ6ODIwMC92MS9wa2kvY2EwLQYDVR0fBCYwJDAioCCgHoYc
aHR0cDovL3ZhdWx0OjgyMDAvdjEvcGtpL2NybDANBgkqhkiG9w0BAQsFAAOCAQEA
IBViCba7Vfy5e5xzL+yI7Vseahc0KVIdMlCVOG2J6lcC2KpcJ9tdpbyQ6/WY6YDD
jNrPMs+a72qXbCmuFWYCVM5nVhwKvFL7jbopd06AGGmweyH97jXGtDAv6TUpkqRA
MZawrx4B7YTjpKzoAben0UP233/K5zR+WeIWysh/9hAESysR/wwxX/IGJj6nmqSp
gv8ybNobXAe1hAfDWQgRJ6bYbawJ0cTcrgEDT1QQyYm3ay1IsWkf6NW4EDQxJG0i
Y90hRKwk4cy8n7QKELOGLqKnUzcxzNMjcpJ8BfE1P6Nq2uL1m2AWJXeMI3hF2S5W
5PxnwmkvBTJVaSikGvoY4Q==
-----END CERTIFICATE-----
private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEArS2Pf7iOOU+hYl/6xU9/N2YxVgjLQD/QFLxMLD9kffzXttzd
CKSppzJmaGDHLnIl18mKFRuBerAqAIMcJQYUI9IM8TGBA5PIwCYOnscLsf1zMu/O
6LHoiRKmUjb0h6AFvmD+UjkMh7Y5kvs18VS1nhSGUVw9CXV9ALD5P+F/55LfcXaG
JEwWPAzjwA5OR7spjkCeGHXRBJjqW6Ct1Oihowrxn015kS0mtZ/gWwxXvG6saC7R
hfl8tXGTGsoFNJ0o+040Wp0rOS+e+Q6GOnIHQKWIFhGM8vZMlWK3bmEahRHZO4s3
XWDgrSNsLORiD6yVT7J6dalsraAAm2je2gJIkQIDAQABAoIBAFCDPxTtM8o3WFuJ
Lehv5kBWVZefLQeo40/Qn0VvD4R3eb69flHXZDykdPIQFGpmjWt+eqEHkbH9lvl3
+yzHX7Oro3K7RjToj0uuJdvxxGEy6U0EKtkKZYbc0dClVhh78E+rfnGxrj6mHKxV
+KVDcdCV0EChNotgQQaCQM9PQozhevTwJTJn6F6k/52Ivy4PrI929D6O5APH2MaJ
Y3mdZCFCBtewPZ/B7RfdFu28rqwfPKwDtru0j/vxN3pZQ5fg20SJ2XPryW/mPNDf
f+cDqiemkHxPczDUPKQZUKNgMizwG501LZB996mCvZADEd3dp2rowV6RSOeqM1n5
ZEr0VnUCgYEA2eCiiJOm1i45kEh6I/utzmPhooOHqnv7eFeBdmdLnQMvAzV8iHsv
LNIjOqWDBB6J4VB/b43mYy2mjRv/7l2+BSep9weD9AuceATOZx+QWw7Gm/1gHMiz
2pleb+ZmQvGAWFS06gFi/G7vR2+2/6F9kLCjcCCdopTtIGVM3U3AcbcCgYEAy3q0
bndayzHRBY84CjYmQR5Cax9Gs928ljvb+9dex0A8Hck+xROK4O2Xy7zqqP/WHeZ8
/V5bnIeoLUc3d3pNn/Il7sBOMge+UMc64Wv23GtmyiDX9P+BtU6EInSwtxW4mgms
aWy7gZde28uH7N7THWK5AHC7xf0DaJ/eB+FL9/cCgYA1eJ/rDPGhFu8hrefr9NSP
FoxFqiodeRgaTL+FI4y3GBTtoK7TgAfv5BKpTf19gVEtbugXpKeqJ4X8k6aYBYGh
Gj7oVXvY5RCdk/Bj9qci8dlkZyazab5aI9G9fLoUK9jn1MIhu/1jHoay7YPn8OY0
IGW8GwUU5Z/cl3/pwC8+uQKBgB325Ok7lFhF7sUF0TfXv4xpW1iRE4VbSvFIwV11
2tQ2xmOQhjjZZuM2udrb6CaY/jwK/C8HnTAQ3hhE24sxrIq4SxO8qAdAEqusmyQl
FQZinpF3grXmhoBfnp/AVWGwxi2Q7R3dUEOGOgbeExczvR0fs6S39T7zwnO+zyCT
8e8DAoGAaDUKgBsk+afVos4jJyeYeO0d6G8zB4tHG1D5ze+AGlMT2RHk/R165YYG
XD0uxw+RFKHyJTUrrQ7/p3lyX8U8O2Fx5pOE/FFIXmZovbLiapEGawbl+SUxeg2z
nnFhAk6cBVXO42xkqgDF5Jk7FyAFsfW/exoXyQxffUWazBZxz6I=
-----END RSA PRIVATE KEY-----
private_key_type    rsa
serial_number       59:85:c1:1b:c4:91:22:e2:ae:02:00:47:33:ff:0c:f5:31:8a:04:39
```
