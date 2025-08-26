@echo off
echo Setting up Python backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo Backend setup complete!
echo.
echo To start the backend server, run:
echo cd backend
echo call venv\Scripts\activate
echo python app.py
pause
