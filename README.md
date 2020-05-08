# This is simple ticket project  
Stay Tuned!

# Niezbędne
> pip install djoser <br>
> pip install djangorestframework-simplejwt <br>
> pip install django-user-accounts <br>
> pip install django <br>
> pip install djangorestframework <br>
> pip install django-registration
# Ręczna aktualizacja bazy
> Usuń db.sqlite3 <br>
> Usuń wszystko z /backend/migrations <br>
> python manage.py makemigrations backend <br>
> python manage.py migrate <br>
> python manage.py createsuperuser <br>
> python manage.py runserver <br>

# Połączenia z serwerem

Serwer został napisany w oparciu o architekturę REST. Połączenie z serwerem nawiązuje się poprzez wywołanie 
adresu url odpowiadającego danej akcji używając przy tym odpowiedniej metody HTTP. Dane w postaci JSON 
przekazuje się poprzez np. metodę POST lub jako zmienną "json" metody GET.

### UWAGA

Do każdego połączenia z serwerem należy dołączyć do adresu zmienną Bearer token postaci
"Authorization: Bearer XXX"


# Kody odpowiedzi

### Sukces
| Kod   | Opis                                           |
| :---: | ---------------------------------------------- |
| 200   | Sukces                                         |
| 201   | Sukces - pomyślnie utworzono obiekt(y)         |

### Błąd
| Kod   | Opis                                                      |
| :---: | --------------------------------------------------------- |
| 400   | Serwer otrzymał złe dane                                  |
| 401   | Serwer nie otrzymał danych                                |
| 404   | Żądany obiekt nie istnieje                                |


## Funkcje

### Sprawdź token
### /auth/jwt/verify
###### Uprawnienia: Każdy

| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia                             | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------- |
| GET         |                  |               |                                              |                                                                                             |
| POST        | application/json | JSON         | {"token" : "XXX"}  | Sprawdzanie tokena                                                                            |
| PUT         |                  |              |                                              | Brak                                                                                        |
| DELETE      |                  |              |                                              | Brak                                                                                        |
> curl -X POST -d '{"token": "XXX"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/auth/jwt/verify

> Sukces: {}
> Niepowodzenie: {"detail":"Token is invalid or expired","code":"token_not_valid"}

### Odśwież
### /auth/jwt/refresh
###### Uprawnienia: Każdy

| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia                             | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------- |
| GET         |                  |               |                                              |                                                                                             |
| POST        | application/json | JSON         | {"refresh" : "XXX"}  | Odświeżanie tokena                                                                       |
| PUT         |                  |              |                                              | Brak                                                                                        |
| DELETE      |                  |              |                                              | Brak                                                                                        |
> curl -X POST -d '{"refresh": "XXX"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/auth/jwt/refresh

> Sukces: {"access":"XXX"} <br>
> Niepowodzenie: {"detail":"Token is invalid or expired","code":"token_not_valid"}

### Rejestracja
### /auth/users/ 
###### Uprawnienia: Każdy

| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia                             | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------- |
| GET         |                  |               |                                              |                                                                                             |
| POST        | application/json | JSON         | {"email": " ","password": " ", "name" : "Tom Hanks", "phone" : "+48123666789"}  | Utworzenie konta                                                                            |
| PUT         |                  |              |                                              | Brak                                                                                        |
| DELETE      |                  |              |                                              | Brak                                                                                        |

> curl -X POST -d '{"email": "arus@arus.com","password": "maslotoniehaslo", "name" : "Tom Hanks", "phone" : "+48123666789"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/auth/users/

### Logowanie
### /auth/jwt/create 
###### Uprawnienia: Każdy
| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | ---------------- | ------------------------------------------------------------------------------------------- |
| GET         |                  |              |                  | Brak                                                                                         |
| POST        | application/json | JSON |        {"email": " ","password": " "}          | Logowanie                                                                                      |
| PUT         |                  |              |                  | Brak                                                                                        |
| DELETE      |                  |              |                  | Brak                                                                                        |

> curl -X POST -d '{"email": "arus@arus.com","password": "maslotoniehaslo"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/auth/jwt/create

### Wydarzenia
### /api/events/
###### Uprawnienia: ?
| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | ---------------- | ------------------------------------------------------------------------------------------- |
| GET         | application/json |              |                  | Pobranie ogólnych informacji (nazwa, data, miejsce) wszystkich wydarzeń                                                                                       |
| POST        | application/json | JSON |        {"id":27, "event_name":"Maraton", "event_date":"2020-12-31T22:00:00+02:00","city":"Wrocław","country": "Polska"} | Dodanie wydarzenia\wydarzeń |
| PUT         |                  |              |                  | Brak                                                                                        |
| DELETE      |                  |              |                  | Brak                                                                                        |

> curl -X GET http://127.0.0.1:8000/api/events/

> curl -X POST -d '{"id":27, "event_name":"Maraton", "event_date":"2020-12-31T22:00:00+02:00","city":"Wrocław","country": "Polska"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/api/events/

### Wydarzenie - szczegóły
### /api/events/<int: id>
###### Uprawnienia: Każdy
| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | ---------------- | ------------------------------------------------------------------------------------------- |
| GET         | application/json |              |                  | Pobranie wszystkich informacji wybranego wydarzenia                                         |
| POST        |                  |              |                  | Brak                                                                                        |
| PUT         |                  |              |                  | Brak                                                                                        |
| DELETE      |                  |              |                  | Brak                                                                                        |

> curl -X GET http://127.0.0.1:8000/api/events/1/