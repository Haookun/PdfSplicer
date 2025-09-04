#!/bin/bash
# 构建macOS App和DMG
# 自动检测依赖、集成bin目录、打包后检测App可运行性

APP_NAME="PdfSplicer"
ENTRY="main.py"
ICON="app_icon.icns" # 如有自定义图标请替换
BIN_DIR="bin"

# Step 0: 安装 requirements.txt 依赖
if [ -f "requirements.txt" ]; then
    echo "正在安装 requirements.txt 依赖..."
    python3 -m pip install -r requirements.txt
fi

# Step 0: 检查依赖
for pkg in pyinstaller dmgbuild; do
    if ! python3 -m pip show $pkg >/dev/null 2>&1; then
        echo "未检测到 $pkg，正在自动安装..."
        python3 -m pip install $pkg
    fi

done

# Step 1: 清理旧产物
rm -rf dist build

# Step 2: 检查bin目录
if [ ! -d "$BIN_DIR" ]; then
    echo "警告：未检测到bin目录，pdftoppm等依赖可能缺失！"
fi

# Step 3: PyInstaller打包App（集成bin目录）
pyinstaller --windowed --name "PdfSplicer" --icon "app_icon.icns" --add-data "bin:bin" --hidden-import PyQt6 "$ENTRY"

# Step 4: dmgbuild生成DMG
if [ -f "dmg_settings.py" ]; then
    dmgbuild -s dmg_settings.py "$APP_NAME" "${APP_NAME}.dmg"
else
    echo "请先准备dmg_settings.py配置文件！"
fi

# Step 5: 打包后检测App是否可运行
APP_EXE="dist/$APP_NAME.app/Contents/MacOS/$APP_NAME"
if [ -f "$APP_EXE" ]; then
    echo "正在检测App启动..."
    "$APP_EXE" > dist/app_test.log 2>&1 &
    sleep 2
    if grep -iE 'error|exception|traceback' dist/app_test.log; then
        echo "警告：App启动检测到异常，请查看 dist/app_test.log 日志！"
    else
        echo "App启动检测通过。"
    fi
else
    echo "未找到App可执行文件，打包可能失败。"
fi

echo "打包完成，App和DMG已生成。"
