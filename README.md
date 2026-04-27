# 🔖 Bookmark Manager

A full-stack Django web application to **save, organize, and manage bookmarks intelligently** with automatic metadata scraping, modern UI, and seamless user authentication.

---

## 🚀 Features

### 📌 Bookmark Management

* Add bookmarks with just a URL
* Automatically fetch:

  * Title
  * Description
  * Favicon
* Delete bookmarks instantly
* Prevent duplicate entries per user

---

### 🔍 Smart Search & Pagination

* Real-time search (HTMX-powered, no page reload)
* Pagination support
* Smooth UX with dynamic updates

---

### 🎨 Modern UI

* Built with **Tailwind CSS**
* Clean dark theme
* Fully responsive (mobile + desktop)

---

### 🔐 Authentication System

* User registration & login
* Google OAuth login (via django-allauth)
* Logout functionality

---

### 🔑 Password Reset

* Email-based password reset flow
* Custom UI (no default Django pages)
* Handles edge case:

  * Users registered via Google cannot reset password

---

## 🧱 Tech Stack

* **Backend:** Django (CBVs)
* **Frontend:** Django Templates + Tailwind CSS
* **Interactivity:** HTMX
* **Authentication:** django-allauth
* **Database:** SQLite (dev) / PostgreSQL (prod-ready)
* **Scraping:** Requests + BeautifulSoup

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/bookmark-manager.git
cd bookmark-manager
```

---

### 2. Create virtual environment

```bash
python -m venv env
source env/bin/activate   # Linux/Mac
env\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup environment variables

Create a `.env` file in root:

```env
SECRET_KEY=your_secret_key
DEBUG=True

# Email (for password reset)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Google OAuth
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_SECRET=your_secret
```

---

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

---

### 7. Run server

```bash
python manage.py runserver
```

---

## 🔑 Google OAuth Setup

1. Go to Google Cloud Console
2. Create OAuth Client ID
3. Add redirect URI:

```text
http://127.0.0.1:8000/accounts/google/login/callback/
```

4. Add credentials in `.env`

---

## 📁 Project Structure

```
bookmark_manager/
│
├── bookmarks/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py   # scraping logic
│   └── templates/
│
├── users/
│   ├── views.py
│   ├── forms.py
│   └── templates/
│
├── templates/
│   ├── base.html
│   └── partials/
│       └── bookmark_list.html
│
├── config/
│   ├── settings.py
│   └── urls.py
│
└── .env
```

---

## 🧠 Key Learnings

* Proper Django form validation using `form.add_error`
* Handling OAuth + traditional auth together
* Debugging migration and DB schema issues
* Building partial rendering with HTMX
* Handling real-world scraping edge cases
* Managing user-specific data securely

---

## 🚀 Future Improvements

* Drag & drop bookmark sorting
* Bookmark categories / tags
* Infinite scroll instead of pagination
* REST API (Django REST Framework)
* Deploy to Render / Railway

---

## 🛡️ Notes

* URLs are normalized (auto-add https)
* Duplicate bookmarks are prevented
* Scraper is fault-tolerant with fallbacks
* Secure handling of password reset edge cases

---

## 🙌 Author

**Inderpreet Singh**

---

⭐ If you like this project, consider starring the repo!
