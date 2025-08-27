<div align="center">
	<img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

# PdfSplicer

你是否在扫描纸质文档时遇到过这样的困扰：正面和反面分别扫描后，面对两份 PDF 文件却不知道如何高效、准确地拼接成一个完整文档？

PdfSplicer 正是为此而生！（天才）
本工具适用于 macOS，拥有简洁易用的图形界面，能够自动识别正反扫描件的页码顺序，智能合并为一个完整的 PDF 文件。无需手动调整，无需繁琐操作，让你的文档整理更高效、更省心。

## 功能特色
- 图形化界面，操作简单
- 支持选择正面和反面扫描件 PDF
- 自动识别并按正确页码顺序拼接
- 支持输出文件夹选择和快速打开
- 一键生成完整 PDF 文件

## 使用方法
<div align="center">
	<img width="400" alt="截屏2025-08-27 15 02 32" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. 前往项目的 [Release 页面](https://github.com/Haookun/PdfSplicer/releases) 下载最新的 `PdfSplicer.dmg` 安装包。
2. 双击打开 DMG 文件，将 `PdfSplicer.app` 拖入 macOS 的“应用程序”文件夹。
3. 在应用程序中启动 PdfSplicer，按界面提示选择正面、反面 PDF 和输出路径，点击“开始拼接”即可。


## 打包与分发（开发者操作指南）
 
 1. 安装打包依赖：
	 ```bash
	 pip install pyinstaller dmgbuild
	 ```
 2. 准备应用图标（建议使用透明背景的 .icns 文件），命名为 `app_icon.icns` 并放在项目根目录。
 3. 使用 PyInstaller 打包为 macOS 应用：
	 ```bash
	 pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
	 ```
	 - 打包后产物在 `dist/PdfSplicer.app` 目录下。
 4. 编写或检查 `dmg_settings.py` 配置文件，确保包含正确的文件、图标、快捷方式等参数。
 5. 使用 dmgbuild 生成 DMG 安装包：
	 ```bash
	 dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
	 ```
	 - 生成的 DMG 文件会在项目根目录或指定路径下。
 6. 建议将最终的 `PdfSplicer.dmg` 文件移动到 `release` 文件夹，方便用户下载和分发。
 7. 用户只需打开 DMG 文件，将 `PdfSplicer.app` 拖入“应用程序”文件夹即可完成安装。
 

## 许可证
MIT License

