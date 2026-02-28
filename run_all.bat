@echo off
chcp 65001 >nul
echo ============================================================
echo   모든 batch_01_img_*.md 파일 차트 자동 생성
echo ============================================================
echo.

REM 파이썬 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo 먼저 Python을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/2] 필요한 라이브러리 확인 중...
pip show pandas >nul 2>&1
if errorlevel 1 (
    echo [정보] 필요한 라이브러리를 설치합니다...
    pip install pandas numpy mplfinance matplotlib
)

echo.
echo [2/2] 차트 생성 시작...
python generate_all_charts.py

if errorlevel 1 (
    echo.
    echo [오류] 차트 생성 중 오류가 발생했습니다.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   완료! 생성된 차트를 확인해주세요.
echo ============================================================
echo.
pause
