# Chat GPT Interrogator

## Short description

API for automatic communication with chatGPT. 
Allows you to send questions and receive answers from chatGPT.


## Requirements

### Reading token from your desktop

You can run api in auto token load mode. All you need is:
- install Chromium (Chrome is not working)
- login to https://chat.openai.com/auth/login


In case of `Cookies file doesn't exist` error, check the path to Chromium cookies - the default path is set to `$user/snap/chromium/common/chromium/Default/Cookies`.

### Running multiple instances of interrogator / manual token transfer

In your's webbrowser cookies find

`chat.openai.com` -> `Cookies` -> `__Secure-next-auth.session-token`

and then transfer the token with one of API's flags.

### API

API requires a specific input file structure. Input data should be prepared as a csv file with following columns:
- `prompt` - a prompt with question to the chatGPT.
- `id` - prompt's id  (optional). Automatically generated if not specified.


Next create a virtual environment, i.e. `virtualenv --python=python3.10 venv` and install requirements:
`pip install -r requirements.txt`. 

Tested on python 3.10.8.

#### Common instalation problems
1) `gevent_socketio` install error -> `pip install -U setuptools & pip install -U wheel`
2) AttributeError: module 'socketio' has no attribute 'AsyncClient' -> `pip install python-socketio`
3) _connect_polling asyncio_client.py 211 [ERROR]: aiohttp not installed -- cannot make HTTP requests! -> `pip install aiohttp`

## Run

1) `python interrogate.py -h` <- Help
2) `python interrogate.py test_data.csv -t 'token_id'` <- Run api with custom token.
3) `python interrogate.py test_data.csv --token-path` <- Run api with custom token loaded from provided file.


---

## Krótki opis

Ulepszone API które umożliwia automatyczne wysyłanie zapytań do czatu GPT

## Wymagania


### Automatyczne korzystanie z tokenu

Obecnie API zintegrowane jest z Chromium (zwykły Chrome niestety nie działa). 
Przed rozpoczęciem scrapowania, należy zalogować się na stronie https://chat.openai.com/auth/login
w zakładce Chromium. Umożliwi to API znalezienie odpowiednich ciasteczek zapisywanych lokalnie.
Jeżeli nawet po zalogowaniu występuje błąd warto odświeżyć stronę pare razy,
i sprawdzić czy https://chat.openai.com/api/auth/session wyświetla informacje o ciasteczku.

Jeżeli pojawi się informacja, że plik Cookies nie istnieje w podanej ścieżce,
lub komunikat "unable to open database file", to należy znaleźćj położenie
Cookies w naszym systemie i podać do skryptu na wejściu (lub zmodyfikować default).


### Wiele tokenów / ręczne podanie tokenu

Uruchomienie API z własnym tokenem umożliwia korzystanie z wielu instancji API na raz. 
Procedura logowania zostaje taka sama. Token można wyciągnąć z ciasteczek w następujący sposób:

W Chromium, w szczegółah odnośnie ciasteczek:

`chat.openai.com` -> `Cookies` -> `__Secure-next-auth.session-token`

Rekomendowane jest logowanie się na kartach incognito. 
Bazując na testach, nie trzeba mieć uruchomionego Chromium w tle - sesja nie przedawnia się.


### API

API przyjmuje pliki csv z dwoma kolumnami:

- `prompt` - zapytanie, które zostanie skierowane do GPT
- `id` - id zapytania (opcjonalne). Jeśli nie zostanie podana to zostanie wygenerowana automatycznie

W kolejnym kroku należy stworzyć wirtualne środowisko np. za pomocą komendy `virtualenv --python=python3.10 venv`,
aktywować je używając `source ./venv/bin/activate` i zainstalować `requirements.txt` używając
`pip install -r requirements.txt`. Aplikacja była testowana na pythonie 3.10.8.


#### Pojawiające się problemy z instalacją
1) `gevent_socketio` nie instaluje się z powodu wewnętrznego błędu pythona -> `pip install -U setuptools & pip install -U wheel`
2) AttributeError: module 'socketio' has no attribute 'AsyncClient' -> `pip install python-socketio`
3) _connect_polling asyncio_client.py 211 [ERROR]: aiohttp not installed -- cannot make HTTP requests! -> `pip install aiohttp`


## Uruchomienie

1) `python interrogate.py test_data.csv` <- podstawowe wywołanie, plik wynikowy zostanie zapisany w folderze **gpt-output**
2) `python interrogate.py test_data.csv -t 'token_id'` <- Uruchomienie API z własnym tokenem
3) `python interrogate.py test_data.csv --token-path` <- Uruchomienie API z własnym tokenem wczytanym z pliku
4) `python interrogate.py -h` <- Wyświetlone zostaną wszystkie opcje uruchomienia


## Dodatkowe informacje

- API działa na zewnętrzym serwerze
- Można uruchomić API kilka razy (z różnymi tokenami)
- Zdażyło się, że po około 26 godzinach zerwało połączenie z serwerem, jednak powinno ono zostać automatycznie zresetowane
- Tokeny są na pewno ważne dłużej niż 3 dni
