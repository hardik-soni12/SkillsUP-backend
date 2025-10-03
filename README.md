# SkillsUP API - Backend  
This repository contains the backend REST API for **SkillsUP**, a skill-sharing application designed to connect users who want to learn a new skill with users who are willing to teach it. The API is built with a professional, multi-environment Flask architecture and features a robust set of features for user management, authentication, and a complete matching and messaging lifecycle.  
  
---
  
## ✨ Key Features  
  
This project is a complete Minimum Viable Product (MVP) with the following features implemented:  
  
▪️ **Secure Authentication System:**  
 Full user registration and login using password hashing (bcrypt) and stateless session management with JSON Web Tokens (JWT), including access and refresh tokens.  
  
▪️ **User & Profile Management:**  
 Full CRUD (Create, Read, Update, Delete) operations for user profiles with secure, owner-only authorization for updates and deletions.  
  
▪️ **Role-Based Access Control:**  
 A working admin role (is_admin flag) with a custom @admin_required decorator to protect sensitive, admin-only endpoints.  
  
▪️ **Core Skill System:**  
 Full CRUD functionality allowing users to add, update, and delete skills they **"know"** and skills they **"want to learn."**  
  

* **Advanced Search & Matching:**  
  
▪️ A dynamic user search endpoint with filters (GET /users?skill_name=...).  
  
▪️ The core **matching algorithm** (GET /matches/suggestions) that proactively finds and suggests mutually beneficial learning partners.  
  
  
* **Full Connection Lifecycle:**  
  
▪️ Users can send "connect" requests (POST /matches).  
  
▪️ Users can view all their incoming, outgoing, and accepted matches (GET /matches).  
  
▪️ Users can accept or reject incoming match requests (PUT /matches/<id>).  
  
▪️ Users can cancel a sent request or unmatch an existing connection (DELETE /matches/<id>).  
  

* **MVP Messaging System:**  
  
▪️ Once a match is accepted, users can send and retrieve messages within that specific connection.  
  

## 🛠️ Tech Stack  
  
▪️ **Framework**: Flask  
  
▪️ **Database**: SQLAlchemy (ORM)  
  
▪️ **Database Migrations**: Flask-Migrate & Alembic  
  
▪️ **Authentication**: Flask-JWT-Extended  
  
▪️ **Data Validation & Serialization**: Marshmallow  
  
▪️ **Automated Testing**: Pytest  
  
▪️ **Environment Management**: python-dotenv, separate configs for Development, Testing, and Production.  
  
  
## 🚀 How to Run Locally  
  
To set up and run this project on your local machine, follow these steps.  
  

### Prerequisites  

▪️ Python 3.10+  
  
▪️ A virtual environment tool (venv)  
  
▪️A database (SQLite is used for development/testing, but it can be configured for PostgreSQL or MySQL)  
  

### Setup Instructions  
  
1. **Clone the repository**:  
bash  
git clone
https://github.com/hardik-soni12/SkillsUP-backend.git  
cd skillsup-backend  
  

2. **Create and activate a virtual environment**:  
  
bash
# For Windows  
python -m venv venv  
.\venv\Scripts\Activate.ps1  
  
bash
# For macOS/Linux  
python3 -m venv venv  
source venv/bin/activate  
  
  
3. **Install the dependencies**:  
  
bash
pip install -r requirements.txt  
  

4. **Set up your environment variables**:  
  
* Create a file named .flaskenv.  
  
* Add the following lines to it to run in development mode:  
  
bash
FLASK_APP=run:app  
FLASK_ENV=development  
  

5. **Set up the database**:  
  
* Run the migration command to create your local dev.db file and all necessary tables.  
  
bash
flask db upgrade  
  
  
6. **Run the application**:  
  
bash
python run.py  
  

The API will now be running at http://127.0.0.1:5000.  
