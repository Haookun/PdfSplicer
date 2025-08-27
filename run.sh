#!/bin/bash
# 该脚本使用必要的Qt插件路径来运行Python应用程序。

# 获取脚本所在的目录，这样就可以从任何地方运行它。
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# 定义虚拟环境中python解释器的完整路径。
PYTHON_EXEC="$SCRIPT_DIR/.venv/bin/python"

# 检查python解释器是否存在。
if [ ! -f "$PYTHON_EXEC" ]; then
    echo "错误：在 $PYTHON_EXEC 未找到Python解释器"
    exit 1
fi

# 定义查找Qt插件路径的命令。
PLUGIN_PATH_CMD="from PyQt6.QtCore import QLibraryInfo; print(QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath))"

# 设置环境变量并运行主脚本。
# 该脚本在运行前会切换到脚本所在的目录。
cd "$SCRIPT_DIR" && QT_QPA_PLATFORM_PLUGIN_PATH=$("$PYTHON_EXEC" -c "$PLUGIN_PATH_CMD") "$PYTHON_EXEC" main.py
