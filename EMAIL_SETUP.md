# 📧 SMTP Email Configuration Guide

This guide will help you configure SMTP email service for sending magic login verification links.

## 🚀 Quick Setup

### Option 1: Using Environment Variables (Recommended)

1. **Create a `.env` file** in your project root (`securefiles/.env`):
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Secure File Share <noreply@securefileshare.com>
```

2. **Install python-decouple** (optional but recommended):
```bash
pip install python-decouple
```

### Option 2: Direct Configuration

Edit `securefiles/settings.py` and replace the email credentials:

```python
EMAIL_HOST_USER = 'your-actual-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 📧 Email Provider Configurations

### Gmail Configuration

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
3. **Use the generated app password** (not your regular password)

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=generated-app-password
```

### Outlook/Hotmail Configuration

```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-password
```

### Yahoo Configuration

1. **Enable 2-Factor Authentication**
2. **Generate App Password**:
   - Account Security → Generate and manage app passwords
   - Create password for "Mail"

```env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yahoo.com
EMAIL_HOST_PASSWORD=generated-app-password
```

## 🧪 Testing Email Configuration

### Method 1: Management Command
```bash
# Show current configuration
python manage.py test_email

# Send test email
python manage.py test_email --test

# Show Gmail setup instructions
python manage.py test_email --provider gmail
```

### Method 2: Django Shell
```bash
python manage.py shell
```

```python
from users.email_utils import test_email_configuration
success, message = test_email_configuration()
print(f"Success: {success}, Message: {message}")
```

### Method 3: Test via Login
1. Register a client user with your real email
2. Login as the client user
3. Check your email for the magic login link

## 🔧 Troubleshooting

### Common Issues:

**1. Authentication Failed**
- For Gmail: Use App Password, not regular password
- Enable 2-Factor Authentication first
- Check EMAIL_HOST_USER format

**2. Connection Timeout**
- Check EMAIL_HOST and EMAIL_PORT
- Verify firewall settings
- Try different ports (25, 465, 587)

**3. TLS/SSL Errors**
- Set EMAIL_USE_TLS=True for port 587
- Set EMAIL_USE_SSL=True for port 465
- Don't use both TLS and SSL

**4. Permission Denied**
- Enable "Less secure app access" (not recommended)
- Use App Passwords instead

### Debug Commands:

```bash
# Check current settings
python manage.py test_email

# Test with verbose output
python manage.py test_email --test --verbosity=2

# Check Django logs
python manage.py runserver --verbosity=2
```

## 🔒 Security Best Practices

1. **Use Environment Variables**: Never commit email credentials to version control
2. **App Passwords**: Use app-specific passwords instead of main account passwords
3. **2-Factor Authentication**: Enable 2FA on your email account
4. **Regular Rotation**: Change app passwords periodically
5. **Limited Scope**: Use dedicated email accounts for applications

## 📁 File Structure

```
securefiles/
├── .env                 # Email credentials (DO NOT COMMIT)
├── .env.example         # Template for email configuration
├── .gitignore          # Includes .env
└── securefiles/
    └── settings.py     # Email configuration
```

## 🎯 Production Considerations

For production deployment:

1. **Use environment variables** from your hosting provider
2. **Configure proper DNS records** (SPF, DKIM, DMARC)
3. **Monitor email delivery rates**
4. **Set up email logging**
5. **Consider dedicated email services** (SendGrid, Mailgun, AWS SES)

## 🆘 Need Help?

1. Run: `python manage.py test_email --provider gmail`
2. Check Django logs during email sending
3. Verify SMTP settings with your email provider
4. Test with a simple email client first

---

✅ Once configured, magic login emails will be sent to real email addresses!
