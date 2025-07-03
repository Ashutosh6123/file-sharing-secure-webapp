# 🛡️ Secure File Share

A Django-based secure file sharing application with verification link authentication, role-based access control, and comprehensive security features.

## 📋 Table of Contents

- [Features](#-features)
- [Authentication System](#-authentication-system)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Security Features](#-security-features)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

## ✨ Features

### 🔐 Advanced Authentication
- **Verification Link Login** - Email-based passwordless authentication
- **Role-Based Access Control** - Separate operations and client user types
- **Single-Use Tokens** - Secure, time-limited access tokens
- **IP & User Agent Tracking** - Comprehensive login audit trail

### 📁 File Management
- **Secure File Upload** - Support for .docx, .pptx, .xlsx files
- **Role-Based File Access** - Operations users can upload, all users can download
- **Unique File Tokens** - Each file has a secure access token
- **Upload History** - Track all file uploads with timestamps

### 🌐 Dual Interface
- **Web Interface** - Beautiful, responsive Bootstrap UI
- **REST API** - Complete API with token authentication
- **Email Integration** - SMTP email delivery with retry mechanism
- **Mobile Responsive** - Works seamlessly on all devices

## 🔑 Authentication System

### Verification Link Flow

1. **User enters email address** on login page
2. **System validates** user exists and is active
3. **Verification link sent** via email with secure token
4. **User clicks link** to authenticate automatically
5. **Role-based redirection** to appropriate dashboard

### User Types

- **🔧 Operations Users** - Can upload and download files
- **👥 Client Users** - Can download files (read-only access)

### Security Features

- ✅ **1-hour token expiration**
- ✅ **Single-use tokens** (cannot be reused)
- ✅ **IP address logging** for audit trails
- ✅ **User agent tracking** for security
- ✅ **Email validation** prevents enumeration attacks
- ✅ **CSRF protection** on all forms

## 📁 Project Structure

```
securefiles/
├── manage.py                    # Django management script
├── db.sqlite3                  # SQLite database
├── .env                        # Environment variables (create from .env.example)
├── requirements.txt            # Python dependencies
│
├── securefiles/                # Main Django project
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
│
├── users/                      # User management app
│   ├── models.py              # User models (CustomUser, MagicLoginToken)
│   ├── views.py               # Authentication views
│   ├── urls.py                # User URL patterns
│   ├── serializers.py         # API serializers
│   ├── utils.py               # Email utilities
│   └── migrations/            # Database migrations
│
├── files/                      # File management app
│   ├── models.py              # File models (UploadedFile)
│   ├── views.py               # File management views
│   ├── urls.py                # File URL patterns
│   └── migrations/            # Database migrations
│
└── templates/                  # HTML templates
    ├── base.html              # Base template
    ├── login.html             # General login
    ├── login_ops.html         # Operations login
    ├── login_client.html      # Client login
    ├── dashboard_ops.html     # Operations dashboard
    ├── dashboard_client.html  # Client dashboard
    └── emails/                # Email templates
        ├── magic_login.html   # HTML email template
        └── magic_login.txt    # Plain text email template
```

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd securefiles
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install django djangorestframework python-dotenv
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your email settings
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

8. **Visit the application**
- Web Interface: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## 🔧 Installation

### Prerequisites

- Python 3.8+
- pip
- Git

### Dependencies

```bash
pip install django==5.2.3
pip install djangorestframework
pip install python-dotenv
```

### Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations users
python manage.py makemigrations files
python manage.py migrate

# Create test users (optional)
python create_test_users.py
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=SecureFileShare <noreply@yoursite.com>

# Security
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3
```

### Email Setup

For Gmail SMTP:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in `EMAIL_HOST_PASSWORD`

For development, emails will display in console if SMTP isn't configured.

## 📖 Usage

### Web Interface

#### For Operations Users:
1. Go to `/ops-login/`
2. Enter your email address
3. Check email for verification link
4. Click link to access operations dashboard
5. Upload files (.docx, .pptx, .xlsx)
6. View all uploaded files

#### For Client Users:
1. Go to `/client-login/`
2. Enter your email address
3. Check email for verification link
4. Click link to access client dashboard
5. View and download available files

### Creating Users

#### Via Django Admin:
1. Access `/admin/`
2. Create new CustomUser
3. Set `is_ops=True` for operations users
4. Set `is_client=True` for client users

#### Via Command Line:
```bash
python create_test_users.py
```

## 🔌 API Documentation

### Authentication

**POST** `/api/login/`
```json
{
    "username": "user@example.com",
    "password": "password"
}
```

**Response:**
```json
{
    "token": "abc123..."
}
```

### Client Signup

**POST** `/api/signup/`
```json
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Email Verification

**GET** `/api/verify-email/{token}/`

### Using API Token

Include in headers:
```
Authorization: Token abc123...
```

## 🛡️ Security Features

### Authentication Security
- **No password storage** for web login
- **Time-limited tokens** (1 hour expiration)
- **Single-use verification links**
- **IP address logging**
- **User agent tracking**
- **CSRF protection**

### File Security
- **Role-based access control**
- **Secure file upload validation**
- **Unique file access tokens**
- **Upload audit trail**

### Email Security
- **Email validation** prevents enumeration
- **Secure token generation** using UUID4
- **SMTP with TLS encryption**
- **Retry mechanism** for reliability

## 🧪 Testing

### Run Test Suite

```bash
# Test verification link functionality
python test_verification_terminology.py

# Test comprehensive login system
python test_final_magic_login.py

# Test email functionality
python test_env_loading.py

# Test role-based redirection
python test_magic_redirection.py
```

### Manual Testing

1. **Create test users:**
```bash
python create_test_users.py
```

2. **Test operations user flow:**
   - Login at `/ops-login/`
   - Check email for verification link
   - Upload a file
   - Verify file appears in dashboard

3. **Test client user flow:**
   - Login at `/client-login/`
   - Check email for verification link
   - View available files
   - Download a file

## 🚀 Deployment

### Production Checklist

1. **Security Settings:**
```python
DEBUG = False
SECRET_KEY = 'production-secret-key'
ALLOWED_HOSTS = ['yourdomain.com']
```

2. **Database:**
   - Use PostgreSQL or MySQL for production
   - Run migrations: `python manage.py migrate`

3. **Static Files:**
```bash
python manage.py collectstatic
```

4. **Email Configuration:**
   - Configure production SMTP server
   - Set up proper `DEFAULT_FROM_EMAIL`

5. **Web Server:**
   - Use Gunicorn + Nginx
   - Configure SSL/TLS certificates
   - Set up proper logging

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/new-feature`
3. **Commit changes:** `git commit -am 'Add new feature'`
4. **Push to branch:** `git push origin feature/new-feature`
5. **Submit Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**Email not sending:**
- Check SMTP configuration in `.env`
- Verify email credentials
- Check firewall/network settings

**Login not working:**
- Ensure user has `is_ops` or `is_client` set to `True`
- Check that user is `is_active=True`
- Verify email address is correct

**File upload failing:**
- Check file format (.docx, .pptx, .xlsx only)
- Ensure user has operations role
- Verify media directory permissions

### Getting Help

- 📧 Email: support@yoursite.com
- 📖 Documentation: [Project Wiki](wiki-url)
- 🐛 Bug Reports: [GitHub Issues](issues-url)

## 🙏 Acknowledgments

- Django framework for the robust foundation
- Bootstrap for the responsive UI components
- Font Awesome for the beautiful icons
- Django REST Framework for API capabilities

---

**Made with ❤️ for secure file sharing**
