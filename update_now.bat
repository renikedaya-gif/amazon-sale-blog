@echo off
chcp 65001 > nul
echo [INFO] ブログを今すぐ更新します...
python "%~dp0scripts\update.py"
if %errorlevel% equ 0 (
    echo.
    echo [完了] index.html を更新しました！
    start "" "%~dp0index.html"
) else (
    echo [ERROR] 更新に失敗しました
)
pause
