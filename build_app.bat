@echo off
chcp 65001 >nul
REM ============================================================
REM PdfSplicer Windows 打包脚本
REM 用法: 双击运行 或 cmd 中执行 build_app.bat
REM 产物: dist\PdfSplicer\ (文件夹模式) 或根据需要修改为单文件
REM ============================================================

set APP_NAME=PdfSplicer
set ENTRY=main.py
set ICON=app_icon.ico
set BIN_DIR=bin

echo ==========================================
echo   PdfSplicer Windows 打包
echo ==========================================

REM ── Step 0: 安装依赖 ──
echo [1/4] 安装依赖...
if exist requirements.txt (
    pip install -r requirements.txt
)
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo   安装 pyinstaller ...
    pip install pyinstaller
)

REM ── Step 1: 清理旧产物 ──
echo [2/4] 清理旧产物...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM ── Step 2: 检查 bin 目录 ──
if not exist "%BIN_DIR%" (
    echo   警告: 未检测到 bin 目录。
    echo   Windows 打包需要 Windows 版本的 poppler 二进制文件。
    echo   请下载 poppler for Windows 并将 pdftoppm.exe 等放入 bin 目录。
    echo   如果不需要空白页检测功能，可忽略此警告。
)

REM ── Step 3: PyInstaller 打包 ──
echo [3/4] PyInstaller 打包中...
if exist "%BIN_DIR%" (
    pyinstaller --windowed --name "%APP_NAME%" --icon "%ICON%" --add-data "%BIN_DIR%;%BIN_DIR%" --hidden-import tkinterdnd2 --hidden-import customtkinter --noconfirm --clean "%ENTRY%"
) else (
    pyinstaller --windowed --name "%APP_NAME%" --icon "%ICON%" --hidden-import tkinterdnd2 --hidden-import customtkinter --noconfirm --clean "%ENTRY%"
)

REM ── Step 4: 验证 ──
echo [4/4] 验证打包结果...
if exist "dist\%APP_NAME%\%APP_NAME%.exe" (
    echo   打包成功!
    echo   可执行文件: dist\%APP_NAME%\%APP_NAME%.exe
) else (
    echo   错误: 未找到可执行文件，打包可能失败。
    exit /b 1
)

echo ==========================================
echo   Windows 打包完成
echo   产物目录: dist\%APP_NAME%\
echo ==========================================
pause
