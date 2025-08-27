# PdfSplicer

<div align="center">
  <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

Haben Sie sich beim Scannen von beidseitigen Dokumenten schon gefragt, wie Sie Vorder- und Rückseiten-PDFs effizient zu einer Datei zusammenfügen?

PdfSplicer löst dieses Problem! Ein intelligentes PDF-Merge-Tool für macOS mit grafischer Oberfläche, erkennt automatisch die Seitenreihenfolge und erstellt ein vollständiges PDF.

## Funktionen
- Einfache grafische Oberfläche
- Auswahl von Vorder- und Rückseiten-PDF
- Automatische Erkennung und Zusammenführung der Seitenreihenfolge
- Auswahl des Ausgabeordners und schnelles Öffnen
- Ein-Klick-Erstellung des vollständigen PDFs

## Anwendung
1. Gehen Sie auf die [Release-Seite](https://github.com/Haookun/PdfSplicer/releases) und laden Sie die neueste `PdfSplicer.dmg` Installationsdatei herunter.
2. Öffnen Sie die DMG-Datei und ziehen Sie `PdfSplicer.app` in den Programme-Ordner.
3. Starten Sie PdfSplicer, wählen Sie Vorder-/Rückseiten-PDF und Ausgabepfad, klicken Sie auf "Zusammenfügen starten".

## Verpackung & Verteilung
1. Abhängigkeiten installieren:
   ```bash
   pip install pyinstaller dmgbuild
   ```
2. Transparentes `.icns`-Icon als `app_icon.icns` im Projektordner bereitstellen.
3. Mit PyInstaller als .app verpacken:
   ```bash
   pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
   ```
   - Ausgabe in `dist/PdfSplicer.app`.
4. `dmg_settings.py` für DMG-Konfiguration prüfen/bearbeiten.
5. DMG erstellen:
   ```bash
   dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
   ```
   - DMG im Projektordner oder angegebenen Pfad.
6. DMG in den `release`-Ordner verschieben.
7. Nutzer zieht `PdfSplicer.app` einfach in Programme zur Installation.

## Lizenz
MIT License

## Repository
https://github.com/Haookun/PdfSplicer
