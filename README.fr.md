<div align="center">
   <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

# PdfSplicer

Vous êtes-vous déjà demandé comment fusionner efficacement les PDF recto et verso d’un document scanné ?

PdfSplicer est là pour vous ! Cet outil intelligent pour macOS propose une interface graphique, reconnaît automatiquement l’ordre des pages et fusionne en un PDF complet.

## Fonctionnalités
- Interface graphique simple
- Sélection des PDF recto et verso
- Reconnaissance et fusion automatiques de l’ordre des pages
- Choix du dossier de sortie et ouverture rapide
- Génération du PDF en un clic
- Saut automatique des pages blanches : option activable, détecte et ignore intelligemment les pages vides pour une fusion plus efficace.

## Utilisation

<div align="center">
   <img width="400" alt="Capture d'écran" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. Rendez-vous sur la [page Release](https://github.com/Haookun/PdfSplicer/releases) et téléchargez le dernier installateur `PdfSplicer.dmg`.
2. Ouvrez le fichier DMG, glissez `PdfSplicer.app` dans le dossier Applications.
3. Lancez PdfSplicer, suivez l’interface pour choisir les PDF recto/verso et le chemin de sortie, puis cliquez sur "Démarrer la fusion".

## Packaging & Distribution

### Script de build automatique

Le projet inclut le script automatique `build_app.sh` pour installer les dépendances, packager l’App, générer le DMG et vérifier le démarrage en une seule commande.

Utilisation :
```bash
bash build_app.sh
```
- Le script installe automatiquement les dépendances de requirements.txt et les outils de build.
- Intègre automatiquement le dossier bin (pdftoppm et autres outils poppler).
- Après le packaging, vérifie le lancement de l’App et écrit les logs dans dist/app_test.log.
- Les artefacts sont dans le dossier dist/ (App) et à la racine du projet (DMG).

Vous pouvez personnaliser les paramètres ou corriger les dépendances en éditant directement `build_app.sh`.

## Licence
MIT License

## Dépannage

- Si vous voyez « pdftoppm introuvable » ou une erreur similaire :
  1. L’application utilise d’abord le dossier bin intégré (déjà inclus).
  2. Pour une installation manuelle, exécutez :
     ```bash
     brew install poppler
     ```
  3. Redémarrez l’application après installation.

## Dépôt
https://github.com/Haookun/PdfSplicer
