@echo off
echo =========================================
echo Urban Oasis Backend Setup Script
echo =========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 4: Creating database migrations...
python manage.py makemigrations

echo.
echo Step 5: Applying migrations...
python manage.py migrate

echo.
echo Step 6: Creating media directories...
mkdir media\gallery 2>nul

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Create an admin user:
echo    python manage.py createsuperuser
echo.
echo 2. Start the development server:
echo    python manage.py runserver
echo.
echo 3. Access the admin panel at:
echo    http://127.0.0.1:8000/admin/
echo.
echo 4. API will be available at:
echo    http://127.0.0.1:8000/api/
echo.
echo =========================================
pause
