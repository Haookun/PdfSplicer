# PdfSplicer

<div align="center">
  <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

¿Alguna vez te has preguntado cómo unir fácilmente los PDFs de anverso y reverso de un documento escaneado?

¡PdfSplicer es la solución! Herramienta inteligente para macOS, interfaz gráfica, reconoce automáticamente el orden de páginas y fusiona en un PDF completo.

## Características
- Interfaz gráfica sencilla
- Selección de PDFs de anverso y reverso
- Reconocimiento y fusión automática del orden de páginas
- Selección de carpeta de salida y apertura rápida
- Generación de PDF con un clic

## Uso
1. Ve a la carpeta `release` y busca el instalador `PdfSplicer.dmg` más reciente.
2. Abre el archivo DMG y arrastra `PdfSplicer.app` a la carpeta de Aplicaciones.
3. Inicia PdfSplicer, selecciona los PDFs de anverso/reverso y la ruta de salida, haz clic en "Iniciar unión".

## Empaquetado y distribución
1. Instala dependencias:
   ```bash
   pip install pyinstaller dmgbuild
   ```
2. Prepara un icono `.icns` transparente llamado `app_icon.icns` en la raíz del proyecto.
3. Empaqueta con PyInstaller:
   ```bash
   pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
   ```
   - Salida en `dist/PdfSplicer.app`.
4. Revisa o edita `dmg_settings.py` para la configuración DMG.
5. Crea el DMG:
   ```bash
   dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
   ```
   - DMG en la raíz del proyecto o ruta especificada.
6. Mueve el DMG a la carpeta `release` para distribución.
7. El usuario solo debe arrastrar `PdfSplicer.app` a Aplicaciones para instalar.

## Licencia
MIT License

## Repositorio
https://github.com/Haookun/PdfSplicer
