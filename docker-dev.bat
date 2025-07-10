@echo off
REM Development Docker Management Script for SecureFiles (Windows)

setlocal enabledelayedexpansion

if "%1"=="" goto usage

if "%1"=="build" goto build
if "%1"=="up" goto up
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="logs" goto logs
if "%1"=="shell" goto shell
if "%1"=="bash" goto bash_shell
if "%1"=="migrate" goto migrate
if "%1"=="superuser" goto superuser
if "%1"=="collect" goto collect
if "%1"=="test" goto test
if "%1"=="clean" goto clean
if "%1"=="status" goto status
if "%1"=="prod" goto prod

goto usage

:usage
echo SecureFiles Docker Management Script
echo.
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   build       Build Docker images
echo   up          Start services in foreground
echo   start       Start services in background
echo   stop        Stop services
echo   restart     Restart services
echo   logs        Show logs
echo   shell       Open Django shell
echo   bash        Open bash shell in web container
echo   migrate     Run Django migrations
echo   superuser   Create Django superuser
echo   collect     Collect static files
echo   test        Run tests
echo   clean       Remove containers and volumes
echo   status      Show container status
echo   prod        Deploy production environment
echo.
goto end

:build
echo Building Docker images...
docker-compose build
echo Build complete!
goto end

:up
echo Starting services...
docker-compose up
goto end

:start
echo Starting services in background...
docker-compose up -d
echo Services started!
docker-compose ps
goto end

:stop
echo Stopping services...
docker-compose down
echo Services stopped!
goto end

:restart
echo Restarting services...
docker-compose restart
echo Services restarted!
goto end

:logs
docker-compose logs -f
goto end

:shell
echo Opening Django shell...
docker-compose exec web python manage.py shell
goto end

:bash_shell
echo Opening bash shell...
docker-compose exec web bash
goto end

:migrate
echo Running migrations...
docker-compose exec web python manage.py migrate
echo Migrations complete!
goto end

:superuser
echo Creating superuser...
docker-compose exec web python manage.py createsuperuser
goto end

:collect
echo Collecting static files...
docker-compose exec web python manage.py collectstatic --noinput
echo Static files collected!
goto end

:test
echo Running tests...
docker-compose exec web python manage.py test
goto end

:clean
set /p confirm=This will remove all containers and volumes. Are you sure? (y/N): 
if /i "!confirm!"=="y" (
    echo Cleaning up...
    docker-compose down -v --remove-orphans
    docker system prune -f
    echo Cleanup complete!
) else (
    echo Cancelled.
)
goto end

:status
echo Container Status:
docker-compose ps
echo.
echo Resource Usage:
docker stats --no-stream
goto end

:prod
echo Deploying production environment...
if not exist .env (
    echo Error: .env file not found. Copy .env.docker to .env and configure it first.
    goto end
)
docker-compose -f docker-compose.prod.yml up -d
echo Production deployment complete!
docker-compose -f docker-compose.prod.yml ps
goto end

:end
