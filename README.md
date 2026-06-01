🛒 Sklep Wielobranżowy – Flask (Python)

Projekt aplikacji webowej sklepu wielobranżowego wykonany w Pythonie z wykorzystaniem frameworka Flask. Aplikacja umożliwia przeglądanie produktów oraz podstawową obsługę sklepu internetowego.

📌 Opis projektu

# 🛒 Sklep Wielobranżowy – Flask (Python) & MongoDB

Projekt aplikacji webowej dwuosobowego zespołu, realizujący w pełni funkcjonalny sklep internetowy. Aplikacja łączy w sobie dynamiczny frontend z bezpiecznym backendem oraz bazą danych NoSQL.

---

## 📌 Opis projektu
Celem projektu było stworzenie wielobranżowego sklepu internetowego jako kompletnej aplikacji webowej. System pozwala na przeglądanie asortymentu podzielonego na kategorie (elektronika, dom, sport, buty, ubrania), wyszukiwanie produktów za pomocą zaawansowanych filtrów (wyrażenia regularne Regex), zarządzanie zawartością koszyka w czasie rzeczywistym oraz finalizację zamówień. Aplikacja posiada także dedykowany i zabezpieczony panel administracyjny do zarządzania zasobami bazy danych (operacje CRUD – dodawanie, edycja, usuwanie towarów).

---

## 👨‍💻 Podział ról w zespole

Zgodnie z wymaganiami projektowymi, zadania zostały równomiernie podzielone pomiędzy autorów projektu, co w pełni odzwierciedla historia commitów na naszych kontach GitHub:

* **Patryk Kudławiec** – *Backend, Logika Biznesowa & Architektura Bazy Danych*
    * Konfiguracja połączenia oraz operacji na bazie danych MongoDB (`utils.db`).
    * Implementacja logiki backendowej: system rejestracji i logowania użytkowników, mechanizm koszyka oraz obsługa zamówień w katalogu `utils/`.
    * Zabezpieczenie sesji użytkownika (historia zakupów) oraz sesji administratora.
    * Wdrożenie walidacji danych po stronie serwera (sprawdzanie formatu adresu, Regex dla kodów pocztowych, walidacja poprawności typów cen).

* **Bartosz Michalak** – *Frontend, Integracja Asynchroniczna & RWD*
    * Przygotowanie semantycznej struktury dokumentów HTML i dynamicznych szablonów Jinja2 (`templates/`).
    * Pełna stylizacja interfejsu w pliku CSS z zachowaniem zasad Responsive Web Design (RWD) dla urządzeń mobilnych i desktopowych.
    * Opracowanie skryptów asynchronicznych w JavaScript (`static/script.js`) komunikujących się z REST API (dynamiczne pobieranie historii, usuwanie pozycji, zmiana ilości bez przeładowywania strony).
    * Wdrożenie walidacji pól formularzy po stronie klienta (atrybuty `required`, `pattern`, `minlength`, `step`).

---

## 🛠️ Technologie i Wymagania

### Backend:
* **Python 3.14+**
* **Flask** – silnik aplikacji, obsługa routingu i zarządzanie sesjami
* **PyMongo** – sterownik do komunikacji z bazą danych MongoDB
* **python-dotenv** – bezpieczne ładowanie zmiennych środowiskowych z pliku `.env`

### Frontend:
* **HTML5 / Jinja2** – semantyczna struktura i renderowanie danych z serwera
* **CSS3** – zaawansowane style wizualne, układy CSS Grid i Flexbox oraz pełne RWD
* **JavaScript (ES6)** – asynchroniczna komunikacja Fetch API z punktami końcowymi aplikacji

### Baza danych (MongoDB):
* Kolekcja **`products`**: przechowuje pełny asortyment (nazwa, opis, cena, kategoria, miniatura, dostępność `active`).
* Kolekcja **`orders`**: rejestruje aktualne koszyki użytkowników (status `delive`) oraz zamówienia pomyślnie sfinalizowane (status `completed`).

---

## 🚀 Uruchomienie projektu

### 1. Klonowanie repozytorium
```bash
git clone [https://github.com/patrykkudlawiec20-creator/zadanie-sklep-wielobranz.git](https://github.com/patrykkudlawiec20-creator/zadanie-sklep-wielobranz.git)
cd zadanie-sklep-wielobranz

2. Utworzenie środowiska wirtualnego

python -m venv venv

Aktywacja:

Windows:

venv\Scripts\activate

Linux / macOS:

source venv/bin/activate

3. Instalacja zależności

pip install flask

lub jeśli masz:

pip install -r requirements.txt

4. Uruchomienie aplikacji

python app.py

5. Otwórz w przeglądarce

http://127.0.0.1:5000/

👨‍💻 Autor

- Patryk Kudławiec
- Bartosz Michalak