
<div align="center">
   <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

# PdfSplicer

両面スキャンしたPDFをどうやって一つにまとめるか悩んだことはありませんか？

PdfSplicerはその悩みを解決します！macOS向けのスマートPDF結合ツールで、グラフィカルなUI、ページ順自動認識、ワンクリックで完全なPDFに統合します。

## 主な機能
- シンプルなグラフィカルUI
- 表裏PDFの選択
- ページ順自動認識・結合
- 出力フォルダ選択・即時オープン
- ワンクリックでPDF生成

## 使い方

<div align="center">
   <img width="400" alt="スクリーンショット" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. [Releaseページ](https://github.com/Haookun/PdfSplicer/releases)で最新の`PdfSplicer.dmg`をダウンロードします。
2. DMGを開き、`PdfSplicer.app`をアプリケーションフォルダにドラッグします。
3. アプリを起動し、表裏PDFと出力先を選択、「開始」ボタンで結合。

## パッケージ・配布
1. 依存インストール:
   ```bash
   pip install pyinstaller dmgbuild
   ```
2. 透明背景の`app_icon.icns`をプロジェクト直下に用意。
3. PyInstallerで.app作成:
   ```bash
   pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
   ```
   - `dist/PdfSplicer.app`に出力。
4. `dmg_settings.py`でDMG設定確認。
5. DMG作成:
   ```bash
   dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
   ```
   - DMGはプロジェクト直下。
6. DMGを`release`フォルダに移動。
7. ユーザーは`PdfSplicer.app`をアプリケーションにドラッグするだけ。

## ライセンス
MIT License

## リポジトリ
https://github.com/Haookun/PdfSplicer
