# Docker Deployment Guide

This guide explains how to deploy the SecureFiles Django application using Docker.

## 🐳 Docker Setup

### Prerequisites
- Docker installed on your system
- Docker Compose installed
- Basic understanding of Docker concepts

### Quick Start (Development)

1. **Build and run the development environment:**
```bash
# Build the Docker image
docker-compose build

# Run the services
docker-compose up

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f web
```

2. **Access the application:**
- Web application: http://localhost:8000
- Database: PostgreSQL on localhost:5432

### Production Deployment

1. **Copy and configure environment variables:**
```bash
# Copy the environment template
cp .env.docker .env

# Edit the .env file with your production values
# IMPORTANT: Change SECRET_KEY, database passwords, email settings
```

2. **Deploy with production configuration:**
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Configuration

### Environment Variables (.env file)

```bash
# Django Settings
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=0
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Settings
POSTGRES_DB=securefiles
POSTGRES_USER=postgres  
POSTGRES_PASSWORD=your-secure-database-password

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=1
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Database Configuration

The application supports both SQLite (development) and PostgreSQL (production):

- **Development**: Uses SQLite by default
- **Production**: Uses PostgreSQL via DATABASE_URL environment variable

## 📋 Docker Commands Reference

### Development Commands
```bash
# Build services
docker-compose build

# Start services
docker-compose up
docker-compose up -d  # detached mode

# Stop services
docker-compose down

# View logs
docker-compose logs -f web
docker-compose logs -f db

# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Shell access
docker-compose exec web bash
docker-compose exec db psql -U postgres -d securefiles
```

### Production Commands
```bash
# Deploy production
docker-compose -f docker-compose.prod.yml up -d

# Update deployment
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Backup database
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres securefiles > backup.sql

# Restore database
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres securefiles < backup.sql
```

## 🗂 Volume Management

### Persistent Data
- **postgres_data**: Database files
- **media_volume**: Uploaded files

### Backup Volumes
```bash
# Backup media files
docker run --rm -v securefiles_media_volume:/data -v $(pwd):/backup alpine tar czf /backup/media-backup.tar.gz -C /data .

# Restore media files
docker run --rm -v securefiles_media_volume:/data -v $(pwd):/backup alpine tar xzf /backup/media-backup.tar.gz -C /data
```

## 🔒 Security Considerations

1. **Change default passwords**
2. **Use strong SECRET_KEY**
3. **Configure proper ALLOWED_HOSTS**
4. **Set up SSL certificates for production**
5. **Use environment variables for sensitive data**
6. **Regular security updates**

## 🚀 SSL/HTTPS Setup (Production)

1. **Obtain SSL certificates:**
```bash
# Using Let's Encrypt (example)
certbot certonly --standalone -d your-domain.com
```

2. **Update nginx.conf:**
   - Uncomment HTTPS server block
   - Update SSL certificate paths
   - Update server_name with your domain

3. **Update docker-compose.prod.yml:**
   - Mount SSL certificates volume
   - Update port mappings

## 🛠 Troubleshooting

### Common Issues

1. **Port already in use:**
```bash
docker-compose down
# Change ports in docker-compose.yml if needed
```

2. **Database connection errors:**
```bash
# Check database is running
docker-compose ps
# Check database logs
docker-compose logs db
```

3. **Permission issues:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

4. **Static files not loading:**
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Logs and Debugging
```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f web
docker-compose logs -f db

# Debug inside container
docker-compose exec web bash
python manage.py shell
```

## 📈 Monitoring and Maintenance

### Health Checks
```bash
# Check container status
docker-compose ps

# Resource usage
docker stats

# Container information
docker-compose exec web python manage.py check
```

### Updates
```bash
# Update application
git pull
docker-compose build web
docker-compose up -d

# Update dependencies
# Edit requirements.txt
docker-compose build web
docker-compose up -d
```

## 🔄 Migration and Scaling

### Database Migrations
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create new migration
docker-compose exec web python manage.py makemigrations
```

### Scaling (Production)
```bash
# Scale web service
docker-compose -f docker-compose.prod.yml up -d --scale web=3

# Use external load balancer for multiple instances
```

This Docker setup provides a complete, production-ready deployment solution for your SecureFiles Django application.
