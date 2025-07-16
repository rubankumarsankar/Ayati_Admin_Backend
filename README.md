# 🚀 FastAPI Admin & Employee Management System

A **FastAPI-based backend** with **JWT authentication**, **role-based access control (RBAC)**, and CRUD operations for **Admins, Employees, and Roles**.  
This project uses **MySQL**, **SQLAlchemy ORM**, and follows best practices for secure and scalable APIs.

---

## 📌 Features
✅ **Admin Authentication (JWT-based)**  
✅ **Super Admin Role** to manage other admins and employees  
✅ **Role Management (Create, Update, Delete Roles)**  
✅ **Employee Management (CRUD, Role Assignment)**  
✅ **Password Hashing (Bcrypt via Passlib)**  
✅ **Token-based Authorization for Protected Routes**  
✅ **MySQL Database with Auto-Migrations**  
✅ **Modular Project Structure (Routes, Models, Schemas, Auth)**

---

## 🛠️ Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)  
- **Database**: MySQL (with SQLAlchemy ORM)  
- **Authentication**: OAuth2 + JWT  
- **Password Hashing**: Passlib (bcrypt)  
- **Migrations**: Alembic (if needed)  
- **Environment Management**: `.env` file

---

## 📂 Project Structure

fastapi-admin-panel/
│
├── app/
│ ├── main.py # FastAPI entry point
│ ├── database.py # DB connection
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ ├── auth.py # JWT & password hashing
│ ├── routes/
│ │ ├── admins.py # Admin routes (login, register, CRUD)
│ │ ├── employees.py # Employee routes
│ │ └── roles.py # Role management
│ └── utils/ # (Optional utilities)
│
├── .env # Environment variables (ignored in git)
├── .gitignore # Git ignore file
├── README.md # Project documentation
└── requirements.txt # Python dependencies

---

## ⚙️ Installation & Setup

### 1️⃣ **Clone the repository**
```bash
git clone https://github.com/rubankumarsankar/Ayati_Admin_Frontend.git
cd fastapi-admin-panel
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

```
### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt

```
### 4️⃣ Configure Environment Variables

Create a .env file in the project root:

```bash
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/admin_panel_db

```

### 5️⃣ Run Database Migrations (Auto-create tables)

# Tables will auto-create when starting FastAPI due to SQLAlchemy
6️⃣ Run the FastAPI server
```bash
uvicorn app.main:app --reload
```
### 🔗 API Documentation
Once the server is running, visit:
```bash
Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc
```

### 📝 Default Admin Creation
When you register the first admin via /admins/register, it will automatically become a Super Admin.

Only Super Admins can create other admins or manage employees.