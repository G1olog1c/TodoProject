# Lista zadań / To-Do List

[🇵🇱 Polski](#-polski) · [🇬🇧 English](#-english)

---

## 🇵🇱 Polski

Aplikacja webowa do zarządzania zadaniami osobistymi, napisana w Django.
Każdy użytkownik ma własną listę zadań z możliwością ustawienia priorytetu i terminu wykonania.

### Funkcje

- 🔐 Rejestracja i logowanie użytkowników
- ➕ Dodawanie, edycja i usuwanie zadań (CRUD)
- ✅ Oznaczanie zadań jako wykonane bez przeładowania strony (AJAX)
- 🎯 Trzy poziomy priorytetu: Niski, Średni, Wysoki
- 📅 Termin wykonania z podświetleniem przeterminowanych i nadchodzących zadań
- 🔍 Wyszukiwanie po tytule i opisie
- 🗂️ Filtrowanie: Wszystkie / Aktywne / Wykonane (z licznikami)
- ↕️ Sortowanie po dowolnej kolumnie (rosnąco / malejąco)
- 🌐 Interfejs w języku polskim
- 📱 Responsywny design (Bootstrap 5)

### Stos technologiczny

- **Python** 3.10+
- **Django** 5.2
- **SQLite** (domyślna baza danych)
- **Bootstrap** 5.3 (CDN)
- **Bootstrap Icons** 1.11

### Instalacja

#### 1. Sklonuj repozytorium

```bash
git clone <https://github.com/G1olog1c/TodoProject.git>
cd POwJP
```

#### 2. Utwórz i aktywuj wirtualne środowisko

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

#### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

#### 4. Wykonaj migracje bazy danych

```bash
python manage.py migrate
```

#### 5. Utwórz konto administratora (opcjonalne)

```bash
python manage.py createsuperuser
```

#### 6. Uruchom serwer deweloperski

```bash
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem: **http://127.0.0.1:8000/**

Panel administracyjny: **http://127.0.0.1:8000/admin/**

### Struktura projektu

```
POwJP/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── todoproject/             # Konfiguracja projektu Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tasks/                   # Aplikacja zarządzania zadaniami
    ├── models.py            # Model Task
    ├── views.py             # Widoki CRUD i AJAX
    ├── urls.py              # Routing aplikacji
    ├── admin.py             # Konfiguracja panelu admina
    └── templates/
        ├── tasks/           # Szablony zadań
        └── registration/    # Logowanie i rejestracja
```

### Jak korzystać

1. Otwórz `http://127.0.0.1:8000/` w przeglądarce
2. Zarejestruj nowe konto (lub zaloguj się)
3. Kliknij **+ Nowe zadanie**, aby dodać pierwsze zadanie
4. Ustaw priorytet i opcjonalnie termin wykonania
5. Korzystaj z wyszukiwarki, filtrów i sortowania, aby zarządzać listą
6. Kliknij checkbox po lewej, aby oznaczyć zadanie jako wykonane


---

## 🇬🇧 English

A web application for managing personal tasks, built with Django.
Each user has their own task list with the ability to set priority and due date.

### Features

- 🔐 User registration and authentication
- ➕ Add, edit and delete tasks (CRUD)
- ✅ Mark tasks as done without page reload (AJAX)
- 🎯 Three priority levels: Low, Medium, High
- 📅 Due dates with highlighting for overdue and upcoming tasks
- 🔍 Search by title and description
- 🗂️ Filtering: All / Active / Done (with counters)
- ↕️ Sort by any column (ascending / descending)
- 🌐 Polish-language interface
- 📱 Responsive design (Bootstrap 5)

### Tech Stack

- **Python** 3.10+
- **Django** 5.2
- **SQLite** (default database)
- **Bootstrap** 5.3 (CDN)
- **Bootstrap Icons** 1.11

### Installation

#### 1. Clone the repository

```bash
git clone <https://github.com/G1olog1c/TodoProject.git>
cd POwJP
```

#### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Apply database migrations

```bash
python manage.py migrate
```

#### 5. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

#### 6. Run the development server

```bash
python manage.py runserver
```

The app will be available at: **http://127.0.0.1:8000/**

Admin panel: **http://127.0.0.1:8000/admin/**

### Project structure

```
POwJP/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── todoproject/             # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tasks/                   # Task management app
    ├── models.py            # Task model
    ├── views.py             # CRUD and AJAX views
    ├── urls.py              # App routing
    ├── admin.py             # Admin panel configuration
    └── templates/
        ├── tasks/           # Task templates
        └── registration/    # Login and signup pages
```

### Usage

1. Open `http://127.0.0.1:8000/` in your browser
2. Register a new account (or sign in)
3. Click **+ Nowe zadanie** to add your first task
4. Set the priority and optionally a due date
5. Use search, filters and sorting to manage your list
6. Click the checkbox on the left to mark a task as completed
