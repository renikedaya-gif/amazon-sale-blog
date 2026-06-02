@echo off
chcp 65001 > nul
echo ===================================
echo  Amazon セールブログ 自動更新セットアップ
echo ===================================
echo.

REM Pythonの場所を確認
where python > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python が見つかりません。
    echo https://www.python.org からインストールしてください。
    pause
    exit /b 1
)

echo [OK] Python が見つかりました
python --version

REM 必要なライブラリをインストール
echo.
echo [INFO] 必要なライブラリをインストール中...
pip install requests jinja2 --quiet
echo [OK] インストール完了

REM 現在のディレクトリを取得
set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%scripts\update.py

echo.
echo [INFO] タスクスケジューラに登録中...

REM 毎時間実行するタスクを作成（既存のタスクがあれば削除してから作成）
schtasks /delete /tn "AmazonSaleBlog_Update" /f > nul 2>&1

schtasks /create ^
  /tn "AmazonSaleBlog_Update" ^
  /tr "python \"%PYTHON_SCRIPT%\"" ^
  /sc HOURLY ^
  /mo 1 ^
  /st 00:00 ^
  /ru "%USERNAME%" ^
  /rl HIGHEST ^
  /f

if %errorlevel% equ 0 (
    echo [OK] タスクスケジューラへの登録が完了しました！
    echo      毎時間 自動でブログを更新します。
) else (
    echo [WARN] タスクスケジューラの登録に失敗しました。
    echo        管理者権限で実行してみてください。
)

echo.
echo === 初回更新を実行します ===
python "%PYTHON_SCRIPT%"

echo.
echo ===================================
echo  セットアップ完了！
echo  index.html をブラウザで開いてください。
echo ===================================
echo.
pause
