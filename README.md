# ✍️ Flask Blog Website 

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

A fully functional, full-stack blogging platform built with **Python** and **Flask**. This application allows users to register, securely log in, and perform full CRUD (Create, Read, Update, Delete) operations on blog posts and comments. It features a rich text editor, user avatars, and a fully responsive frontend utilizing the "Clean Blog" Bootstrap theme.

---

## ✨ Features

- **User Authentication:** Secure user registration, login, and logout using `Flask-Login` and `Werkzeug` (scrypt password hashing).
- **CRUD Operations:** Users can create, read, edit, and delete their own blog posts.
- **Commenting System:** Authenticated users can leave comments on posts. Comments can also be deleted.
- **Rich Text Editing:** Integrated `Flask-CKEditor` for writing beautifully formatted blog posts.
- **Relational Database:** Powered by SQLite and `Flask-SQLAlchemy` with established relationships between Users, Posts, and Comments.
- **User Avatars:** Automatically generates user profile pictures using `Flask-Gravatar` based on registered email addresses.
- **Contact Form:** Working contact form that sends messages directly to your email using `smtplib`.
- **Responsive UI:** Styled with **Bootstrap 5** and Jinja2 templating for a seamless experience on all devices.

---

## 🛠️ Tech Stack

**Backend:**
- Python
- Flask
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication Management)
- SQLite (Database)
- Werkzeug (Password Hashing)

**Frontend:**
- HTML5 / CSS3
- Jinja2 (Templating Engine)
- Bootstrap 5 (Styling & Responsiveness)
- Flask-CKEditor (Rich Text Input)
- Flask-Gravatar (Avatars)

---

## ⚙️ Getting Started

Follow these steps to set up and run the project locally on your machine.

### Prerequisites
Make sure you have [Python](https://www.python.org/downloads/) (v3.8 or higher) and `pip` installed.

### 1. Clone the repository
```bash
git clone https://github.com/MuhammadAhmadgeek/Blogs_Website.git
cd Blogs_Website
