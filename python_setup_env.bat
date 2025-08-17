@echo off
setlocal

:: Name of virtual environment folder
set VENV_NAME=venv

echo ===========================================
echo   Creating virtual environment: %VENV_NAME%
echo ===========================================
python -m venv %VENV_NAME%

echo.
echo ===========================================
echo   Activating virtual environment...
echo ===========================================
call %VENV_NAME%\Scripts\activate.bat

echo.
echo ===========================================
echo   Installing Python packages inside venv...
echo ===========================================
pip install --upgrade pip

:: Core packages for data analysis
pip install pandas numpy matplotlib requests jupyter

:: Discord bot packages
pip install discord.py python-dotenv

:: Extras: web scraping, better CLI, etc.
pip install beautifulsoup4 lxml ipython rich

echo.
echo ===========================================
echo ✅ Setup complete!
echo 📁 Virtual Environment: %VENV_NAME%
echo ▶️ To activate, run: %VENV_NAME%\Scripts\activate
echo ❌ To exit venv, type: deactivate
echo ===========================================
pause
