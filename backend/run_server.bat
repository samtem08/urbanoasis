@echo off
cd /d "C:\Users\ADMIN\Desktop\urbanoasisapartment\urban_oasis_backend"
call venv\Scripts\activate.bat
python manage.py runserver 8000
pause
