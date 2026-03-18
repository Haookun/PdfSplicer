#!/bin/bash
# ============================================================
# PdfSplicer 一键打包脚本 (macOS / Linux)
# 自动检测平台并执行对应打包流程
# 用法: bash build_all.sh
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  PdfSplicer 一键打包"
echo "============================================"

OS="$(uname -s)"
case "$OS" in
    Darwin)
        echo "  检测到 macOS 平台"
        echo ""
        bash build_app.sh
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "  检测到 Windows 平台 (Git Bash / MSYS)"
        echo ""
        cmd //c build_app.bat
        ;;
    Linux)
        echo "  检测到 Linux 平台"
        echo "  使用 macOS 构建流程（不含 DMG 步骤）..."
        echo ""

        echo "[1/3] 安装依赖..."
        pip install -r requirements.txt
        pip show pyinstaller >/dev/null 2>&1 || pip install pyinstaller

        echo "[2/3] PyInstaller 打包中..."
        rm -rf dist build
        BIN_OPTS=""
        [ -d "bin" ] && BIN_OPTS="--add-data bin:bin"
        pyinstaller \
            --windowed \
            --name "PdfSplicer" \
            --hidden-import tkinterdnd2 \
            --hidden-import customtkinter \
            --noconfirm \
            --clean \
            $BIN_OPTS \
            main.py

        echo "[3/3] 验证..."
        if [ -f "dist/PdfSplicer/PdfSplicer" ]; then
            echo "  打包成功! 产物: dist/PdfSplicer/"
        else
            echo "  打包可能失败，请检查日志。"
        fi
        ;;
    *)
        echo "  不支持的平台: $OS"
        exit 1
        ;;
esac

echo ""
echo "============================================"
echo "  打包流程结束"
echo "============================================"
