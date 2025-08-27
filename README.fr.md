# PdfSplicer

<div align="center">
  <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

Vous êtes-vous déjà demandé comment fusionner efficacement les PDF recto et verso d’un document scanné ?

PdfSplicer est là pour vous ! Cet outil intelligent pour macOS propose une interface graphique, reconnaît automatiquement l’ordre des pages et fusionne en un PDF complet.

## Fonctionnalités
- Interface graphique simple
- Sélection des PDF recto et verso
- Reconnaissance et fusion automatiques de l’ordre des pages
- Choix du dossier de sortie et ouverture rapide
- Génération du PDF en un clic

## Utilisation
1. Rendez-vous dans le dossier `release` et trouvez le dernier installateur `PdfSplicer.dmg`.
2. Ouvrez le fichier DMG, glissez `PdfSplicer.app` dans le dossier Applications.
3. Lancez PdfSplicer, suivez l’interface pour choisir les PDF recto/verso et le chemin de sortie, puis cliquez sur "Démarrer la fusion".

## Packaging & Distribution
1. Installer les dépendances :
   ```bash
   pip install pyinstaller dmgbuild
   ```
2. Préparez une icône transparente `.icns` nommée `app_icon.icns` à la racine du projet.
3. Emballez avec PyInstaller :
   ```bash
   pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
   ```
   - Résultat dans `dist/PdfSplicer.app`.
4. Vérifiez ou modifiez `dmg_settings.py` pour la configuration DMG.
5. Créez le DMG :
   ```bash
   dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
   ```
   - DMG dans la racine du projet ou le chemin spécifié.
6. Déplacez le DMG dans le dossier `release` pour la distribution.
7. L’utilisateur n’a qu’à glisser `PdfSplicer.app` dans Applications pour installer.

## Licence
MIT License

## Dépôt
https://github.com/Haookun/PdfSplicer
