# Tweetify

A Twitter/X-inspired social media web application built with Django. Users can post, edit, delete, and view "tweets" — each with a title, description, and optional image.

---

## Features

- **View Feed** — Browse all tweets on the home page
- **Create Tweets** — Post new tweets with a title, description, and optional image upload
- **Edit Tweets** — Update the content or image of any existing tweet
- **Delete Tweets** — Remove tweets from the feed
- **User Authentication** — Login system powered by Django's built-in auth

---

## Tech Stack

| Layer       | Technology                     |
|-------------|-------------------------------|
| Backend     | Python 3.10+, Django 5.0       |
| Database    | SQLite (default)               |
| Frontend    | Django Templates, HTML/CSS     |
| Fonts/Icons | Inter (Google Fonts), Font Awesome |
| Images      | Pillow (via Django ImageField) |
| Package Mgr | Poetry                         |

---

## Project Structure

```
tweet/                        # Main Django project root
├── manage.py                 # Django management entry point
├── tweet/                    # Project configuration
│   ├── settings.py           # Django settings (DB, media, installed apps)
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py
└── two/                      # Core application
    ├── models.py             # Tweet data model
    ├── views.py              # CRUD logic and authentication
    ├── urls.py               # App URL routes
    └── templates/            # HTML templates
        ├── index.html        # Tweet feed (home page)
        ├── add.html          # Create tweet form
        ├── edit_tweet.html   # Edit tweet form
        └── login.html        # Login page
media/
└── details/                  # Uploaded tweet images stored here
```

---

## Data Model

**`tweet`** (defined in `tweet/two/models.py`)

| Field    | Type          | Description                          |
|----------|---------------|--------------------------------------|
| `user`   | ForeignKey    | Links tweet to a Django User (optional) |
| `tittle` | TextField     | Tweet title (max 50 characters)      |
| `desc`   | TextField     | Tweet body/description               |
| `imag`   | ImageField    | Optional image upload                |

---

## URL Routes

| URL Pattern                        | View            | Name           | Description         |
|------------------------------------|-----------------|----------------|---------------------|
| `/`                                | `index`         | `index`        | Home feed           |
| `/add_tweet/`                      | `add_tweet`     | `add_tweet`    | Create a new tweet  |
| `/edit_tweet/<id>/`                | `edit_tweet`    | `edit_tweet`   | Edit a tweet        |
| `/delete_tweet/<id>/`              | `delete_tweet`  | `delete_tweet` | Delete a tweet      |
| `/login/`                          | `login`         | `login`        | Login page          |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry installed (`pip install poetry`)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Apply database migrations**
   ```bash
   cd tweet
   python manage.py migrate
   ```

4. **Create a superuser** (optional, for Django admin)
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser** and visit `http://127.0.0.1:8000/`

---

## Media / Image Uploads

Uploaded images are stored in `tweet/media/details/`. Django's `MEDIA_URL` and `MEDIA_ROOT` settings must be configured in `settings.py` to serve them correctly in development:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## Authentication

The app uses Django's built-in `authenticate` and `login` functions. To access protected actions, log in via `/login/`. A superuser account can also be managed through the Django admin panel at `/admin/`.

---

## Dependencies

Defined in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
python = "^3.10"
Django = "^5.0"
```

> Pillow is required for image uploads. Install it if not already present:
> ```bash
> poetry add Pillow
> ```

---

## License

This project is for personal/educational use.
