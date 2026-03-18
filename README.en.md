<div align="center">
   <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

# PdfSplicer

Are you troubled when scanning double-sided documents, not knowing how to efficiently merge the front and back PDFs into one?

PdfSplicer is designed for this! This is a smart PDF merging tool for macOS, featuring a modern CustomTkinter interface with drag-and-drop support, automatically recognizing page order and merging into a complete PDF.

## Features
- Modern CustomTkinter interface, clean and elegant
- Drag-and-drop or click to select PDF files
- Select front and back scanned PDFs
- Automatically recognize and merge in correct page order
- Choose output folder and open quickly
- One-click to generate complete PDF
- Auto skip blank pages: Optional switch, uses white-pixel ratio analysis to intelligently detect and skip blank pages (including near-white scanned pages), improving merging efficiency.

## Usage

<div align="center">
	<img width="400" alt="截屏2026-03-18 11 51 43" src="https://github.com/user-attachments/assets/7669efb5-6c34-4a64-a59c-9176ec11cc26" />
</div>

1. Go to the [Release page](https://github.com/Haookun/PdfSplicer/releases) and download the latest `PdfSplicer.dmg` installer.
2. Double-click the DMG file, drag `PdfSplicer.app` into the Applications folder.
3. Launch PdfSplicer, follow the interface to select front/back PDFs and output path, then click "Start Merging".

## Packaging & Distribution

### One-click Build Script

The project includes an automatic build script `build_app.sh` for one-click dependency installation, App packaging, DMG generation, and startup check.

Usage:
```bash
bash build_app.sh
```
- The script will automatically install dependencies from requirements.txt and all build tools.
- Automatically integrates the bin directory (pdftoppm and other poppler tools).
- After packaging, it checks if the App can run and outputs logs to dist/app_test.log.
- Artifacts are in the dist/ folder (App) and project root (DMG).

You can customize parameters or fix dependencies by editing `build_app.sh` directly.

## License
MIT License

## Troubleshooting

- If you see "pdftoppm not found" or related errors:
  1. The app will first use the built-in bin directory (already integrated).
  2. If manual installation is needed, run:
     ```bash
     brew install poppler
     ```
  3. Restart the app after installation.

## Repository
https://github.com/Haookun/PdfSplicer
