@echo off
chcp 65001 > nul
title GOOGLE INDEX CHECKER - PLAYWRIGHT CHROMIUM ENGINE

echo ===============================================================
echo        GOOGLE INDEX CHECKER - PLAYWRIGHT BROWSER ENGINE
echo ===============================================================
echo.
echo [*] Dang khoi chay cong cu kiem tra Google Index...
echo [*] Vui long dam bao ban da dan danh sach URL vao file urls.txt
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [-] LOI: Python chua duoc cai dat hoac chua duoc them vao PATH!
    echo [-] Vui long cai dat Python va thu lai.
    pause
    exit /b 1
)

python -m playwright install chromium >nul 2>&1

python check_index.py

echo.
echo ===============================================================
echo [+] HOAN THANH! File bao cao Excel da duoc tao o thu muc nay.
echo ===============================================================
pause
