#!/bin/bash

# Development Docker Management Script for SecureFiles

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_color() {
    printf "${1}${2}${NC}\n"
}

# Print usage
usage() {
    print_color $BLUE "SecureFiles Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build       Build Docker images"
    echo "  up          Start services in foreground"
    echo "  start       Start services in background"
    echo "  stop        Stop services"
    echo "  restart     Restart services"
    echo "  logs        Show logs"
    echo "  shell       Open Django shell"
    echo "  bash        Open bash shell in web container"
    echo "  migrate     Run Django migrations"
    echo "  superuser   Create Django superuser"
    echo "  collect     Collect static files"
    echo "  test        Run tests"
    echo "  clean       Remove containers and volumes"
    echo "  status      Show container status"
    echo "  prod        Deploy production environment"
    echo ""
}

# Build images
build() {
    print_color $YELLOW "Building Docker images..."
    docker-compose build
    print_color $GREEN "Build complete!"
}

# Start services in foreground
up() {
    print_color $YELLOW "Starting services..."
    docker-compose up
}

# Start services in background
start() {
    print_color $YELLOW "Starting services in background..."
    docker-compose up -d
    print_color $GREEN "Services started!"
    docker-compose ps
}

# Stop services
stop() {
    print_color $YELLOW "Stopping services..."
    docker-compose down
    print_color $GREEN "Services stopped!"
}

# Restart services
restart() {
    print_color $YELLOW "Restarting services..."
    docker-compose restart
    print_color $GREEN "Services restarted!"
}

# Show logs
logs() {
    docker-compose logs -f
}

# Open Django shell
shell() {
    print_color $BLUE "Opening Django shell..."
    docker-compose exec web python manage.py shell
}

# Open bash shell
bash_shell() {
    print_color $BLUE "Opening bash shell..."
    docker-compose exec web bash
}

# Run migrations
migrate() {
    print_color $YELLOW "Running migrations..."
    docker-compose exec web python manage.py migrate
    print_color $GREEN "Migrations complete!"
}

# Create superuser
superuser() {
    print_color $BLUE "Creating superuser..."
    docker-compose exec web python manage.py createsuperuser
}

# Collect static files
collect() {
    print_color $YELLOW "Collecting static files..."
    docker-compose exec web python manage.py collectstatic --noinput
    print_color $GREEN "Static files collected!"
}

# Run tests
test() {
    print_color $YELLOW "Running tests..."
    docker-compose exec web python manage.py test
}

# Clean up
clean() {
    print_color $RED "This will remove all containers and volumes. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_color $YELLOW "Cleaning up..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_color $GREEN "Cleanup complete!"
    else
        print_color $BLUE "Cancelled."
    fi
}

# Show status
status() {
    print_color $BLUE "Container Status:"
    docker-compose ps
    echo ""
    print_color $BLUE "Resource Usage:"
    docker stats --no-stream
}

# Production deployment
prod() {
    print_color $YELLOW "Deploying production environment..."
    if [[ ! -f .env ]]; then
        print_color $RED "Error: .env file not found. Copy .env.docker to .env and configure it first."
        exit 1
    fi
    docker-compose -f docker-compose.prod.yml up -d
    print_color $GREEN "Production deployment complete!"
    docker-compose -f docker-compose.prod.yml ps
}

# Main script logic
case "$1" in
    build)
        build
        ;;
    up)
        up
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    shell)
        shell
        ;;
    bash)
        bash_shell
        ;;
    migrate)
        migrate
        ;;
    superuser)
        superuser
        ;;
    collect)
        collect
        ;;
    test)
        test
        ;;
    clean)
        clean
        ;;
    status)
        status
        ;;
    prod)
        prod
        ;;
    *)
        usage
        exit 1
        ;;
esac
