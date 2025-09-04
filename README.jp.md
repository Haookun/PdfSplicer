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
- 空白ページ自動スキップ：オプションで有効化可能。内容解析により空白ページを自動判定して除外、効率アップ。

## 使い方

<div align="center">
   <img width="400" alt="スクリーンショット" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. [Releaseページ](https://github.com/Haookun/PdfSplicer/releases)で最新の`PdfSplicer.dmg`をダウンロードします。
2. DMGを開き、`PdfSplicer.app`をアプリケーションフォルダにドラッグします。
3. アプリを起動し、表裏PDFと出力先を選択、「開始」ボタンで結合。

## パッケージ・配布

### ワンクリック自動ビルドスクリプト

本プロジェクトには自動ビルドスクリプト `build_app.sh` が含まれており、依存インストール・Appパッケージ化・DMG生成・起動チェックを一括実行できます。

使い方：
```bash
bash build_app.sh
```
- スクリプトは requirements.txt とビルド関連依存を自動インストールします。
- binディレクトリ（pdftoppm等popplerツール）を自動集成。
- パッケージ後、Appの起動可否をチェックし、ログを dist/app_test.log に出力。
- 生成物は dist/ フォルダ（App）とプロジェクト直下（DMG）に保存されます。

パラメータや依存修正は `build_app.sh` を直接編集してください。

## ライセンス
MIT License

## トラブルシューティング

- 「pdftoppmが見つかりません」等のエラーが出た場合：
  1. まず内蔵binディレクトリ（自動同梱）を利用します。
  2. 手動インストールが必要な場合は、以下を実行：
     ```bash
     brew install poppler
     ```
  3. インストール後アプリを再起動してください。

## リポジトリ
https://github.com/Haookun/PdfSplicer
