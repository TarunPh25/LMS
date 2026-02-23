
<div align="center">

# 🎓 LMS Pro — Student Management System

> *Where education meets elegance. Built with FastAPI, PostgreSQL & a modern UI.*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

</div>

---

## 🌟 What is LMS Pro?

**LMS Pro** is a full-stack, industry-grade **Learning Management System** designed to give institutions and educators a clean, powerful interface to manage their student lifecycle — from enrollment to graduation.

It features a **RESTful FastAPI backend** paired with **two frontend options**: a slick Vanilla JS SPA and a traditional Flask server-rendered application. Everything is backed by a rock-solid **PostgreSQL** database with support for soft deletes, data validation, and automatic timestamps.

---

## ✨ Feature Highlights

| Feature | Details |
|---|---|
| 🔁 **Full CRUD** | Create, Read, Update & Delete students via REST API |
| 🛡️ **Soft Deletes** | Students are never truly erased — they're safely archived |
| 📋 **Status Tracking** | `active` · `inactive` · `suspended` · `graduated` |
| 🔍 **Live Search** | Instant client-side filtering by name or email |
| 📊 **Stats Dashboard** | Real-time cards showing total, active & graduated students |
| 🔔 **Toast Notifications** | Success/error feedback on every action |
| 📦 **Auto Schema Migration** | Tables are created automatically on startup via SQLAlchemy |
| ✅ **Email Validation** | Powered by Pydantic's `EmailStr` — no duplicates allowed |
| 🌐 **CORS Ready** | Configured for cross-origin frontend communication |
| 📘 **Interactive API Docs** | Swagger UI & ReDoc shipped out of the box by FastAPI |

---

## 🗂️ Project Structure

```
📦 2.LMS/
│
├── 🐍 main.py                     ← FastAPI backend (port 8001)
│
├── 🌐 frontend_modern/            ← Modern SPA (Vanilla JS)
│   ├── index.html                 ← Main dashboard layout
│   ├── style.css                  ← Custom dark-themed design system
│   └── app.js                     ← Fetch-based API integration
│
└── 🧪 flask_frontend/             ← Classic SSR frontend (Flask)
    ├── app.py                     ← Flask app (port 5000)
    ├── requirements.txt           ← Flask dependencies
    └── templates/
        ├── base.html              ← Layout shell
        ├── index.html             ← Student listing
        ├── create.html            ← Create student form
        ├── detail.html            ← Student detail view
        └── edit.html              ← Edit student form
```

---

## ⚡ Quick Start

### Prerequisites

Make sure you have the following installed:

- ✅ **Python 3.10+**
- ✅ **PostgreSQL 14+** (running locally on port `5432`)
- ✅ **pip** package manager

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/TarunPh25/2.LMS.git
cd 2.LMS
```

---

### 2️⃣ Set Up the Backend (FastAPI)

```bash
pip install fastapi uvicorn sqlalchemy pydantic psycopg2-binary "pydantic[email]"
```

> 📝 **Update your database credentials** inside `main.py`:
> ```python
> DATABASE_URL = "postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/YOUR_DB"
> ```

```bash
python main.py
```

🟢 Backend is now live at → **http://127.0.0.1:8001**
📚 Explore the API at → **http://127.0.0.1:8001/docs**

---

### 3️⃣ Launch the Modern Frontend (SPA)

Simply open `frontend_modern/index.html` in your browser:

```bash
open frontend_modern/index.html
```

> The SPA connects to port `8001` by default. Make sure the backend is running.

---

### 4️⃣ Launch the Flask Frontend (Optional)

```bash
cd flask_frontend
pip install -r requirements.txt
python app.py
```

🟢 Flask app running at → **http://127.0.0.1:5000**

---

## 🔌 API Reference

All endpoints are prefixed at `http://127.0.0.1:8001`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/students/` | List all active students (supports `?status=` & pagination) |
| `POST` | `/students/` | Register a new student |
| `GET` | `/students/{id}` | Get a specific student by ID |
| `PUT` | `/students/{id}` | Update student information |
| `DELETE` | `/students/{id}` | Soft-delete a student (reversible) |
| `DELETE` | `/students/{id}/hard` | Permanently remove a student ⚠️ |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | Alternative ReDoc documentation |

---

### 📬 Example: Create a Student

```bash
curl -X POST http://127.0.0.1:8001/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@university.edu",
    "phone": "+1 555 000 1234",
    "date_of_birth": "2002-07-15",
    "status": "active"
  }'
```

### 📬 Example: Filter by Status

```bash
curl "http://127.0.0.1:8001/students/?status=graduated&limit=50"
```

---

## 🛢️ Data Model

```
students
├── id              INTEGER        PRIMARY KEY, auto-increment
├── first_name      VARCHAR(100)   NOT NULL
├── last_name       VARCHAR(100)   NOT NULL
├── email           VARCHAR(255)   UNIQUE, NOT NULL
├── phone           VARCHAR(20)    OPTIONAL
├── date_of_birth   DATE           OPTIONAL
├── enrollment_date DATE           DEFAULT: today
├── status          VARCHAR(20)    DEFAULT: 'active'
├── created_at      TIMESTAMPTZ    DEFAULT: now()
├── updated_at      TIMESTAMPTZ    AUTO-UPDATED on change
└── is_deleted      BOOLEAN        DEFAULT: false  ← soft delete flag
```

---

## 🎨 Frontend Architecture

### Modern SPA (`frontend_modern/`)
- Pure **Vanilla JS** — no framework, no build step required
- **Outfit** font from Google Fonts for a premium typographic feel
- **Font Awesome 6** icons for clear affordance on every action
- Responsive **sidebar navigation** with status-based filtering
- **Modal-based form** for creating and editing students
- **Toast notification** system for real-time feedback

### Flask SSR (`flask_frontend/`)
- Classic **server-rendered** HTML with Jinja2 templates
- Communicates with the FastAPI backend via Python `requests`
- Flash message system for form validation feedback
- Multi-page CRUD flow: list → detail → create/edit/delete

---

## 🔐 Security Notes

> ⚠️ Before going to production, please:

- [ ] Change the Flask `secret_key` in `flask_frontend/app.py`
- [ ] Restrict `allow_origins` in CORS middleware to your actual domain
- [ ] Store `DATABASE_URL` in environment variables (never hardcode credentials)
- [ ] Add authentication middleware (JWT / OAuth2)
- [ ] Enable HTTPS with a valid TLS certificate

---

## 🛣️ Roadmap

- [ ] 🔐 JWT Authentication & role-based access (Admin / Teacher / Student)
- [ ] 📂 Course & enrollment management module
- [ ] 📊 Analytics dashboard with charts
- [ ] 📧 Email notifications on status changes
- [ ] 🐳 Docker Compose setup for one-command deployment
- [ ] 🧪 Pytest unit & integration test suite

---

## 🤝 Contributing

Contributions are always welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request 🚀

---

## 👨‍💻 Author

<div align="center">

**Tarun Phogat**

[![GitHub](https://img.shields.io/badge/GitHub-TarunPh25-181717?style=for-the-badge&logo=github)](https://github.com/TarunPh25)

*Built with ❤️ and a lot of ☕*

</div>

---

<div align="center">

⭐ **If this project helped you, consider giving it a star!** ⭐

</div>
