#!/bin/bash
# ============================================================
# PdfSplicer macOS 打包脚本
# 用法: bash build_app.sh
# 产物: dist/PdfSplicer.app + PdfSplicer.dmg
# ============================================================
set -e

APP_NAME="PdfSplicer"
ENTRY="main.py"
ICON="app_icon.icns"
BIN_DIR="bin"

echo "=========================================="
echo "  PdfSplicer macOS 打包"
echo "=========================================="

# ── Step 0: 安装依赖 ──
echo "[1/5] 安装依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
for pkg in pyinstaller dmgbuild; do
    if ! python3 -m pip show "$pkg" >/dev/null 2>&1; then
        echo "  安装 $pkg ..."
        pip install "$pkg"
    fi
done

# ── Step 1: 清理旧产物 ──
echo "[2/5] 清理旧产物..."
rm -rf dist build "${APP_NAME}.dmg"

# ── Step 2: 检查 bin 目录 ──
if [ ! -d "$BIN_DIR" ]; then
    echo "  警告: 未检测到 bin 目录，pdftoppm 等依赖可能缺失！"
fi

# ── Step 3: PyInstaller 打包 ──
echo "[3/5] PyInstaller 打包中..."
pyinstaller \
    --windowed \
    --name "$APP_NAME" \
    --icon "$ICON" \
    --add-data "$BIN_DIR:$BIN_DIR" \
    --hidden-import tkinterdnd2 \
    --hidden-import customtkinter \
    --noconfirm \
    --clean \
    "$ENTRY"

# ── Step 4: 生成 DMG ──
echo "[4/5] 生成 DMG..."
if [ -f "dmg_settings.py" ]; then
    dmgbuild -s dmg_settings.py "$APP_NAME" "${APP_NAME}.dmg"
    echo "  DMG 已生成: ${APP_NAME}.dmg"
else
    echo "  跳过 DMG 生成 (未找到 dmg_settings.py)"
fi

# ── Step 5: 验证 ──
echo "[5/5] 验证打包结果..."
APP_EXE="dist/$APP_NAME.app/Contents/MacOS/$APP_NAME"
if [ -f "$APP_EXE" ]; then
    echo "  App 可执行文件已生成: $APP_EXE"
    echo "  打包成功!"
else
    echo "  错误: 未找到 App 可执行文件，打包可能失败。"
    exit 1
fi

echo "=========================================="
echo "  macOS 打包完成"
echo "  App: dist/${APP_NAME}.app"
[ -f "${APP_NAME}.dmg" ] && echo "  DMG: ${APP_NAME}.dmg"
echo "=========================================="
