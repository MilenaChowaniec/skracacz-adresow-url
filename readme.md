# Skracacz adresów URL
Aplikacja webowa do skracania długich adresów URL, napisana w Flask.

## Opis projektu
Skracacz adresów URL to aplikacja webowa, która:
1. Skraca długie adresy URL do krótkich kodów za pomocą kodowania Base62.
2. Tworzy skrócony link przekierowujący na oryginalny adres URL.
3. Zapisuje listę wszystkich skróconych adresów URL w bazie.
4. Umożliwia usunięcie skróconych adresów URL.

## Technologie
1. **Python**
2. **Flask**
3. **Flask-SQLAlchemy** - ORM do obsługi bazy danych
4. **SQLite** - baza danych
5. **base-62** - biblioteka do kodowania 
6. **pytest** - framework do testów jednostkowych
7. **Docker** 
8. **Validators** 

## Instalacja i uruchomienie za pomocą Docker
**Uruchomienie:**
```bash
git clone https://github.com/MilenaChowaniec/url-shortener.git
cd url-shortener

docker-compose up app

# Aplikacja dostępna pod adresem:
# http://localhost:5000
```

**Zatrzymanie:**
```bash
# Ctrl+C w terminalu lub:
docker-compose down
```

## Testy
Projekt zawiera 11 testów:
- 10 testów jednostkowych (unit tests)
- 1 kompleksowy test całej aplikacji

**Uruchomienie testów:**
```bash
docker-compose up test
```

**Uruchomienie testów i aplikacji:**
```bash
docker-compose up app-test

```
