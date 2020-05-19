# This is simple ticket project  
Stay Tuned!

# Niezbędne
> pip install djoser <br>
> pip install djangorestframework-simplejwt <br>
> pip install django-user-accounts <br>
> pip install django <br>
> pip install djangorestframework <br>
> pip install django-registration <br>
> pip install django-filter
> pip install django-qr-code

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
| 204   | Sukces - pomyślnie usunięto obiekt             |

### Błąd
| Kod   | Opis                                                      |
| :---: | --------------------------------------------------------- |
| 400   | Serwer otrzymał złe dane                                  |
| 401   | Serwer nie otrzymał danych                                |
| 403   | Brak uprawnień                                            |
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
### /api/events
###### Uprawnienia: GET - każdy, POST - admin
| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | ---------------- | ------------------------------------------------------------------------------------------- |
| GET         |                  |              |                  | Pobranie podstawowych informacji (nazwa, data, miejsce) wszystkich wydarzeń                                                                                       |
| POST        | application/json | JSON         |{"event_name":"Maraton",   "descriptions":"Opis wydarzenia",   "pictures":"https://strona.pl/adres/url/zdjecia.jpg",    "event_date":"2020-04-17T11:22:42+02:00",    "city":"Wrocław",    "street":"Długa",    "post_code":"53-615",    "street_address":"1",    "country":"Polska"} | Dodanie wydarzenia\wydarzeń |
| (PUT)       |                  |              |                  | Brak                                                                                        |
| (DELETE)    |                  |              |                  | Brak                                                                                        |

> curl -X GET http://127.0.0.1:8000/api/events/

### Filtrowanie i sortowanie wydarzeń: /api/events/?
| Parametr wydarzenia | HTTP - filtrowanie |  HTTP - sortowanie   |
| ------------------- | ------------------ | -------------------- |
| ID                  | ?id=               | ?ordering=id         |
| Nazwa               | ?event_name=       | ?ordering=event_name |
| Opis                | ?descriptions=     |                      |
| Data                | ?event_date=       | ?ordering=event_date |
| Miasto              | ?city=             | ?ordering=city       |
| Ulica               | ?street=           |                      |
| Państwo             | ?country=          | ?ordering=country    |
Aby sortować malejąco użyj znaku: -= (?ordering-=id)

> curl -X GET http://127.0.0.1:8000/api/events/?street=Kolorowa&country=Polska
>
> curl -X GET http://127.0.0.1:8000/api/events/?ordering=event_date

### Szczegóły wydarzenia
### /api/events/<int: id>
###### Uprawnienia: GET - każdy, PUT, DELETE - admin
| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | ---------------- | ------------------------------------------------------------------------------------------- |
| GET         |                  |              |                  | Pobranie wszystkich informacji wybranego wydarzenia                                         |
| (POST)      |                  |              |                  | Brak                                                                                        |
| PUT         | application/json |JSON          |{"event_name":"Maraton",   "descriptions":"Zaktualizowany opis",   "pictures":"https://strona.pl/adres/url/zdjecia.jpg",    "event_date":"2020-04-17T11:22:42+02:00",    "city":"Wrocław",    "street":"Długa",    "post_code":"53-615",    "street_address":"1",    "country":"Polska"} | Aktualizacja informacji o wybranym wydarzeniu|       
| DELETE      |                  |              |                  | Usunięcie wybranego wydarzenia                                                                                       |

> curl -X GET http://127.0.0.1:8000/api/events/1/

### Bilety
### /api/tickets
###### Uprawnienia: admin
| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | ---------------- | ------------------------------------------------------------------------------------------- |
| GET         |                  |              |                  | Pobranie podstawowych infromacji o wszystkich biletach                                      |
| (POST)      |                  |              |                  | Brak                                                                                        |
| (PUT)       |                  |              |                  | Brak                                                                                        |       
| (DELETE)    |                  |              |                  | Brak                                                                                        |

> curl -X GET http://127.0.0.1:8000/api/tickets/

### Szczegóły biletu
### /api/tickets/<int: id>
###### Uprawnienia: admin
| Metoda HTTP | Content-Type     | Opis wejścia | Przykład wejścia | Akcja                                                                                       |
| ----------- | ---------------- | ------------ | ---------------- | ------------------------------------------------------------------------------------------- |
| GET         |                  |              |                  | Pobranie wszystkich informacji wybranego biletu                                             |
| (POST)      |                  |              |                  | Brak                                                                                        |
| PUT         | application/json |JSON          |                  | Aktualizacja informacji o wybranym bilecie                                                  |       
| DELETE      |                  |              |                  | Usunięcie wybranego biletu                                                                  |

> curl -X GET http://127.0.0.1:8000/api/tickets/1/
