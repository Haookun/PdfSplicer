# PdfSplicer

<div align="center">
  <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

Are you troubled when scanning double-sided documents, not knowing how to efficiently merge the front and back PDFs into one?

PdfSplicer is designed for this! This is a smart PDF merging tool for macOS, with a graphical interface, automatically recognizing page order and merging into a complete PDF.

## Features
- Simple graphical interface
- Select front and back scanned PDFs
- Automatically recognize and merge in correct page order
- Choose output folder and open quickly
- One-click to generate complete PDF

## Usage
1. Go to the `release` folder and find the latest `PdfSplicer.dmg` installer.
2. Double-click the DMG file, drag `PdfSplicer.app` into the Applications folder.
3. Launch PdfSplicer, follow the interface to select front/back PDFs and output path, then click "Start Merging".

## Packaging & Distribution
1. Install dependencies:
   ```bash
   pip install pyinstaller dmgbuild
   ```
2. Prepare a transparent `.icns` icon named `app_icon.icns` in the project root.
3. Package with PyInstaller:
   ```bash
   pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
   ```
   - Output in `dist/PdfSplicer.app`.
4. Check or edit `dmg_settings.py` for DMG config.
5. Build DMG:
   ```bash
   dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
   ```
   - DMG will be in project root or specified path.
6. Move DMG to `release` folder for distribution.
7. Users just need to drag `PdfSplicer.app` into Applications to install.

## License
MIT License

## Repository
https://github.com/Haookun/PdfSplicer
