
# PdfSplicer

一个适用于 macOS 的 PDF 正反扫描件智能拼接工具，支持图形界面，自动识别页码顺序并合并为完整 PDF。

## 功能特色
- 图形化界面，操作简单
- 支持选择正面和反面扫描件 PDF
- 自动识别并按正确页码顺序拼接
- 支持输出文件夹选择和快速打开
- 一键生成完整 PDF 文件

## 使用方法
1. 安装依赖：
	 ```bash
	 pip install -r requirements.txt
	 ```
2. 运行主程序：
	 ```bash
	 python main.py
	 ```
3. 按界面提示选择正面、反面 PDF 和输出路径，点击“开始拼接”即可。

## 打包与分发
- 使用 PyInstaller 打包为 .app：
	```bash
	pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
	```
- 使用 dmgbuild 生成 DMG 安装包：
	```bash
	dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
	```

## 许可证
MIT License

## 开源地址
（待上传后补充）
