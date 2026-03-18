<div align="center">
   <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

# PdfSplicer

Haben Sie sich beim Scannen von beidseitigen Dokumenten schon gefragt, wie Sie Vorder- und Rückseiten-PDFs effizient zu einer Datei zusammenfügen?

PdfSplicer löst dieses Problem! Ein intelligentes PDF-Merge-Tool für macOS mit moderner CustomTkinter-Oberfläche und Drag-and-Drop-Unterstützung, erkennt automatisch die Seitenreihenfolge und erstellt ein vollständiges PDF.

## Funktionen
- Moderne CustomTkinter-Oberfläche, schlicht und elegant
- Drag-and-Drop oder Klick zur PDF-Auswahl
- Auswahl von Vorder- und Rückseiten-PDF
- Automatische Erkennung und Zusammenführung der Seitenreihenfolge
- Auswahl des Ausgabeordners und schnelles Öffnen
- Ein-Klick-Erstellung des vollständigen PDFs
- Automatisches Überspringen leerer Seiten: Optional aktivierbar, nutzt Weißpixel-Verhältnisanalyse zur intelligenten Erkennung und Überspringung leerer Seiten (einschließlich fast weißer Scannerseiten) für effizienteres Zusammenfügen.

## Anwendung

<div align="center">
   <img width="400" alt="Screenshot" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. Gehen Sie auf die [Release-Seite](https://github.com/Haookun/PdfSplicer/releases) und laden Sie die neueste `PdfSplicer.dmg` Installationsdatei herunter.
2. Öffnen Sie die DMG-Datei und ziehen Sie `PdfSplicer.app` in den Programme-Ordner.
3. Starten Sie PdfSplicer, wählen Sie Vorder-/Rückseiten-PDF und Ausgabepfad, klicken Sie auf "Zusammenfügen starten".

## Verpackung & Verteilung

### Automatisches Build-Skript

Das Projekt enthält das automatische Build-Skript `build_app.sh`, mit dem Sie mit einem Klick Abhängigkeiten installieren, die App packen, DMG erstellen und den Start prüfen können.

Verwendung:
```bash
bash build_app.sh
```
- Das Skript installiert automatisch alle Abhängigkeiten aus requirements.txt und die Build-Tools.
- Integriert automatisch das bin-Verzeichnis (pdftoppm und andere Poppler-Tools).
- Nach dem Packaging wird geprüft, ob die App läuft, und das Log nach dist/app_test.log geschrieben.
- Die Artefakte befinden sich im dist/-Ordner (App) und im Projektverzeichnis (DMG).

Parameter und Abhängigkeiten können direkt in `build_app.sh` angepasst werden.

## Lizenz
MIT License

## Fehlerbehebung

- Bei „pdftoppm nicht gefunden“ oder ähnlichen Fehlern:
  1. Die App nutzt zuerst das integrierte bin-Verzeichnis (bereits enthalten).
  2. Für manuelle Installation:
     ```bash
     brew install poppler
     ```
  3. Nach der Installation die App neu starten.

## Repository
https://github.com/Haookun/PdfSplicer
