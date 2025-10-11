@echo off
setlocal enabledelayedexpansion

:: !! ファイル名がぶつかってリネームできないときはこっち使って !!

:: 引数がない場合のエラー処理
if "%~1"=="" (
    echo 使用方法: rename_images.bat [フォルダパス]
    exit /b
)

set "target_dir=%~1"

:: フォルダが存在するか確認
if not exist "%target_dir%" (
    echo 指定されたフォルダが存在しません: %target_dir%
    exit /b
)

:: 末尾にバックスラッシュがあれば削除
if "%target_dir:~-1%"=="\" set "target_dir=%target_dir:~0,-1%"

:: フォルダ名を取得
for %%A in ("%target_dir%") do set "folder_name=%%~nA"

echo 対象フォルダ: %target_dir%
echo リネーム開始...

set /a counter=1

for %%F in ("%target_dir%\*") do (
    if not "%%~aF"=="d" (
        set "ext=%%~xF"
        set "num=00!counter!"
        set "num=!num:~-3!"
        set "newname=%folder_name%-b!num!!ext!"
        echo %%~nxF → !newname!
        ren "%%F" "!newname!"
        set /a counter+=1
    )
)

echo 完了しました。
pause
