# CodingWorld - A Blog Platform for Coders

**CodingWorld** is a blog website designed for developers to share coding knowledge, tutorials, and insights. Built with **Flask** and **MySQL**, it provides a user-friendly platform where coders can publish and manage blogs while engaging with the community.

## 📌 Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Installation Instructions](#installation-instructions)
4. [How to Use](#how-to-use)
5. [Project Structure](#project-structure)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgements](#acknowledgements)

---

## ✨ Features

### User Authentication
- **Signup**: Users can register using their email and password.
- **Login & Logout**: Secure authentication system with session management.
- **Password Hashing**: Secure storage using **PBKDF2** encryption.

### Blog Management System
- **Users can**:
  - Create, edit, and delete blog posts.
  - Upload blog posts with a **Title, Image, Category, Summary, and Content**.
  - View a list of their own published blogs.
- **Visitors can**:
  - Browse published blog posts.
  - View categorized blog lists with title, images, and summaries.

### Other Features
- **Categorized Blogs**: Easily filter blog posts by topic.
- **Responsive UI**: Optimized for mobile and desktop devices.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MySQL
- **Authentication & Security**: Flask-Session, PBKDF2
- **Version Control**: Git

---

## 🚀 Installation Instructions

### Prerequisites
Before installing, ensure you have:
- **Python 3.x** installed ([Download Python](https://www.python.org/downloads/))
- **pip** package manager
- **MySQL** installed ([Download MySQL](https://dev.mysql.com/downloads/installer/))
- **Virtual Environment** (optional but recommended)

### Steps to Install

1️⃣ **Clone the repository**:
```bash
git clone https://github.com/imrj18/CodingWorld.git
cd CodingWorld
```

2️⃣ **Set up a virtual environment** (recommended):

For **Windows**:
```bash
python -m venv .venv
.venv\Scripts\activate
```

For **Linux/macOS**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3️⃣ **Install dependencies**:
```bash
pip install -r requirements.txt
```

4️⃣ **Configure the database**:
Create a MySQL database and update your `.env` file with your credentials:

```env
DB_URI=mysql://<username>:<password>@localhost/<database_name>
```

Example:
```env
DB_URI=mysql://root:password@localhost/codingworld
```

5️⃣ **Run database migrations**:
```bash
flask db init
flask db migrate
flask db upgrade
```

6️⃣ **Run the application**:
```bash
flask run
```

Now, open `http://127.0.0.1:5000/` in your browser to access CodingWorld.

---

## 📖 How to Use

### User Features
1. **Signup**:
   - Register using your email and password.
   - Your credentials are securely stored with encryption.

2. **Login**:
   - Enter your credentials to access the blog dashboard.

3. **Logout**:
   - Securely log out from the application.

### Blog Features
1. **Create a Blog**:
   - Navigate to the blog creation page and enter the required details.
   - Upload an image and categorize the blog.

2. **Manage Blogs**:
   - Edit or delete blogs from your dashboard.

3. **View Blogs**:
   - Browse categorized blogs from various developers.

---

## 📂 Project Structure

```
CodingWorld/
│
├── app.py               # Main application logic
├── templates/           # HTML templates
│   ├── home.html        # Homepage
│   ├── login.html       # Login page
│   ├── signup.html      # Signup page
│   ├── create_blog.html # Blog creation form
│   ├── edit_blog.html   # Edit blog form
│   ├── view_blog.html   # Single blog view
│   ├── blogs.html       # List of all blogs
│
├── static/              # Static assets (CSS, images)
├── models.py            # Database models (User, Blog)
├── migrations/          # Flask database migrations
├── requirements.txt     # Required dependencies
├── .gitignore           # Ignore unnecessary files
└── README.md            # Project documentation
```

---

## 🤝 Contributing

1. **Fork the repository**.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/CodingWorld.git
   cd CodingWorld
   ```
3. **Create a new branch**:
   ```bash
   git checkout -b feature-name
   ```
4. **Commit your changes**:
   ```bash
   git commit -m "Add new feature"
   ```
5. **Push to your branch**:
   ```bash
   git push origin feature-name
   ```
6. **Submit a pull request** 🚀.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgements

- **Flask Documentation**: [Flask Docs](https://flask.palletsprojects.com/)
- **Bootstrap**: [Bootstrap Docs](https://getbootstrap.com/)
