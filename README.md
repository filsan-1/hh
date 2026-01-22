<h1 align="center">
    Hormone Harmony ::
</h1>

## Tech Stack:

<img src="https://img.shields.io/badge/html5%20-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white"/> <img src="https://img.shields.io/badge/css3%20-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white"/> <img src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white"/> <img src="https://img.shields.io/badge/markdown-%23000000.svg?&style=for-the-badge&logo=markdown&logoColor=white"/> <img src="https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white"/> <img src ="https://img.shields.io/badge/sqlite-%2307405e.svg?&style=for-the-badge&logo=sqlite&logoColor=white"/>


<p align="center">
    ✨ Welcome to Hormone Harmony ✨ <br />
  
  ![](https://static.vecteezy.com/system/resources/previews/002/683/683/large_2x/group-of-women-together-diversity-or-multicultural-vector.jpg)
    
</p>
<br />



- **Frontend:** Html,Css
- **Backend:** Django
- **Version Control:** Git and GitHub
- **Code Editor and tools**: VS Code




# Table of Contents

    - Overview
    - Features
    - Future Prospects
    - Setup Guidelines
    - Contribution Guideline
    

## Overview 🔨
Hormone Harmony is a platform where women with any hormonal issue come together to blog and share recipes. You can track your hormonal health and receive notifications about your menstrual cycles. Remember, you are not alone. Let's debunk myths, share self-care tips, and support each other on this journey.

## Features:

- [x] Sign up, Login, Logout with form validation
- [x] Write Blog with image uploads
- [x] Edit and delete blog posts
- [x] Like and comment on blogs
- [x] View blog details with comments
- [x] Create, edit, and delete recipes
- [x] Recipe sharing with cooking instructions, ingredients, and timing
- [x] Track period cycles with custom period tracking
- [x] Log symptoms and health data
- [x] View period history and details
- [x] Edit Profile with profile picture
- [x] Information about PCOS and self-care tips
- [x] Frequently asked questions
- [x] Contact section
- [x] Support circle for community discussions
- [x] Messaging system between users
- [x] Admin dashboard for content management
- [x] Responsive design for all devices
- [x] Custom template tags for enhanced functionality
- [x] Spousal education
- [x] **Enterprise-level security with Argon2 password encryption**
- [x] **Rate limiting to prevent brute force attacks**
- [x] **Secure session management and CSRF protection**

## 🔒 Security Features

We take your security seriously. This application includes several layers of protection:

**Password Security:**
- Your passwords are encrypted using Argon2, the most secure password hashing algorithm available today
- All passwords are automatically hashed and can never be viewed by anyone, including administrators
- Strong password requirements: minimum 12 characters with complexity rules

**Login Protection:**
- Rate limiting prevents brute force attacks (5 attempts per 5 minutes)
- Automatic account lockout after multiple failed attempts
- Secure session management with automatic timeout after 1 hour of inactivity

**Data Protection:**
- HTTPS/SSL support for encrypted communication
- CSRF protection on all forms to prevent cross-site attacks
- Secure cookie handling with HTTP-only flags
- File upload validation (size and type checking)

**Additional Security:**
- Security headers to prevent clickjacking and XSS attacks
- Content Security Policy implementation
- Environment-based configuration to keep secrets safe

## ⚡ Setup Guidelines

**Quick Start:**

1. Clone the repository:
```bash
git clone https://github.com/filsan-1/hh.git
cd hh
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Create static files directory:
```bash
python manage.py collectstatic --noinput
```

6. Create a superuser (admin account):
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

8. Open your browser and go to `http://localhost:8000`

**Testing Security Features:**

You can verify that password encryption is working properly:
```bash
python manage.py check_password_security
```

This will show you which password hashing algorithm is being used (should be Argon2).


## 🔧 Configuration

For production deployment, create a `.env` file with your settings:
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

See `.env.example` for more configuration options.






-


## Future Prospects:

- Location detection and details of nearby gynecologist.
- Adding a quiz app that will take inputs about periods and give information on what is right and wrong.


