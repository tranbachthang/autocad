@echo off
chcp 65001 >nul
cd /d "%~dp0"
REM Dung goi nay lam "bo nao" cua Pi: nap AGENTS.md + skills/ ngay trong thu muc nay.
set "PI_CODING_AGENT_DIR=%~dp0"
REM Ep Python luon xuat text tieng Viet duoi dang UTF-8 (tranh loi ma hoa tren may khac).
set "PYTHONIOENCODING=utf-8"
echo ============================================
echo   MO PHUOC_JR - TRO LY AI THIET KE CO KHI
echo   (go lenh tieng Viet roi Enter)
echo ============================================
pi
pause
