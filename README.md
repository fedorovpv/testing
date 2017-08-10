# Установка окружения
Для запуска необходимо приложение [Docker](https://docs.docker.com/engine/installation/) с утилитой Docker-Compose.

Для версий Windows выпущенных до Windows 10 необходимо использовать [Docker Toolbox](https://www.docker.com/products/docker-toolbox) и выполнить дополнительную настройку:
  - запустить VirtualBox(устанавливается вместе с Docker);
  - выбрать виртуальную машину default;
  - выбрать "Настроить";
  - выбрать "Сеть";
  - в "дополнительно" выбрать "Проброс портов";
  - добавить правило:
  
|   Имя  | Протокол | Адрес хоста | Порт хоста | Адрес гостя | Порт гостя |
|:------:|:--------:|:-----------:|:----------:|:-----------:|:----------:|
| Rule # |    TCP   |  127.0.0.1  |    5000    |             | 5000       |

Если порт 5000 занят, можно указать другой в "порт хоста".


# Запуск окружения
Выполнить:
  - `cd {директория с приложением}`
  - `docker-compose build`
  - `docker-compose up`
  
_В ОС Windows команды запускать в Docker Quickstart Terminal_

Для проверки работоспособности в браузере ввести в адресной строке `http://localhost:5000`, должно появиться сообщение `It's alive!`


# Задание
## Предусловие
- Загрузить окружение с github.
- Установить и проверить установку согласно README.
- Тест должен быть реализован с помощью Python, Robot Framework.
- Код автотеста выложить в своём репозитории github, приложив лог прогона теста.

- В ./web находится SQLite БД clients.db, которая имеет таблицы:
  - CLIENTS с полями CLIENT_ID и CLIENT_NAME;
  - BALANCES с полями CLIENTS_CLIENT_ID и BALANCE;
- Таблицы CLIENTS и BALANCES связаны "один к одному".
- Clients.db загружается в образ при выполнении команды docker build, поэтому в ходе выполнения теста возникнет разница в хранимых данных, тест должен отловить эту ошибку, если она проявится.
- Тест должен быть построен максимально переносимо, то есть таким образом, чтобы он корректно отрабатывал в разных условиях: например как при отсутствии подходящего клиента в выборке из базы данных, так и при его наличии. Корректность в данном случае включает в себя неуспешное завершение прогона теста, если он отловил ошибку: в этом случае должно быть выведено максимально детализированое сообщение. 


## Шаги
### Шаг 1
Подключиться к SQLite базе данных ./web/clients.db.
### Шаг 2
Составить и выполнить SQL-запрос для выборки из БД клиента с положительным балансом. В случае отсутствия подходящего клиента добавить новую запись с помощью SQL-запроса:
- CLIENT_ID - INTEGER уникальное для поля этой таблицы;
- CLIENT_NAME - произвольный;
- BALANCE = 5.00.

Зафиксировать идентификатор клиента, начальный баланс клиента.

### Шаг 3
Получить список подключённых клиенту услуг, выполнив POST запрос http://localhost:{port}/client/services и передав в теле json с идентификатором клиента и заголовок Content-Type=application/json.

Пример запроса:
```
POST http://localhost:5000/client/services HTTP/1.1
Host: localhost:5000
Connection: keep-alive
Content-Length: 21
Postman-Token: c27d99fd-ef9c-f7bb-7cd8-a60e4045ced1
Cache-Control: no-cache
Origin: chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36
Content-Type: application/json
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,sr;q=0.2
 
 
{
 "client_id": 3
}
```

Пример ответа:
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 110
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 05 Apr 2017 14:52:44 GMT
 
 
{
  "count": 1,
  "items": [
    {
      "cost": 1.2,
      "id": 1,
      "name": "Service #1"
    }
  ]
}
```

Зафиксировать список подключённых клиенту услуг.

### Шаг 4
Получить список всех доступных услуг, выполнив GET запрос http://localhost:{port}/services.

Пример запроса:
```
GET http://localhost:5000/services HTTP/1.1
Host: localhost:5000
Connection: keep-alive
Postman-Token: 7729ce2c-413e-62b5-13ed-ab1e8cdcde42
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36
Content-Type: application/json
Accept: */*
Accept-Encoding: gzip, deflate, sdch, br
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,sr;q=0.2
```
Пример ответа:
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 422
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 05 Apr 2017 15:02:33 GMT
 
 
{
  "count": 5,
  "items": [
    {
      "cost": 1.2,
      "id": 1,
      "name": "Service #1"
    },
    {
      "cost": 0.35,
      "id": 2,
      "name": "Service #2"
    },
    {
      "cost": 0.15,
      "id": 3,
      "name": "Service #3"
    },
    {
      "cost": 0.15,
      "id": 4,
      "name": "Service #4"
    },
    {
      "cost": 0.05,
      "id": 5,
      "name": "Service #5"
    }
  ]
}
```

Зафиксировать список всех доступных услуг.

### Шаг 5
В списке всех доступных услуг найти неподключенную для данного клиента услугу.
Зафиксировать идентификатор услуги, стоимость подключения услуги. 

### Шаг 6
Подключить услугу клиенту, выполнив POST запрос http://localhost:{port}/client/add_service.

Пример запроса:
```
POST http://localhost:5000/client/add_service HTTP/1.1
Host: localhost:5000
Connection: keep-alive
Content-Length: 40
Postman-Token: fc93f4ff-d387-dd06-50ef-e5bac46dbc35
Cache-Control: no-cache
Origin: chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36
Content-Type: application/json
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,sr;q=0.2
 
{
 "client_id": 1,
 "service_id": 1
}
```

Пример ответа:
```
HTTP/1.0 202 ACCEPTED
Content-Type: text/html; charset=utf-8
Content-Length: 10
Server: Werkzeug/0.12.1 Python/2.7.12
Date: Wed, 05 Apr 2017 15:10:12 GMT
Processing
```
#### Ожидаемый результат
Код ответа 202.

### Шаг 7
Выполнять ожидание до тех пор, пока не появится новая услуга. Максимально допустимое время ожидания 1 минута, иначе тест считается проваленным.
#### Ожидаемый результат
Новая услуга отображается в POST запросе http://localhost:{port}/client/services
### Шаг 8
Выбрать из БД баланс клиента.
Зафиксировать конечный баланс клиента.

### Шаг 9	
Сравнить:
  {конечный баланс} = {начальный баланс} - {стоимость подключения услуги}
#### Ожидаемый результат
Значения равны


-----------
Maintainer CJSC "PETER-SERVICE" Pavel Fedorov Pavel.Fedorov@billing.ru
