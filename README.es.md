<div align="center">
   <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

# PdfSplicer

¿Alguna vez te has preguntado cómo unir fácilmente los PDFs de anverso y reverso de un documento escaneado?

¡PdfSplicer es la solución! Herramienta inteligente para macOS con interfaz moderna CustomTkinter y soporte de arrastrar y soltar, reconoce automáticamente el orden de páginas y fusiona en un PDF completo.

## Características
- Interfaz moderna CustomTkinter, limpia y elegante
- Arrastrar y soltar o hacer clic para seleccionar archivos PDF
- Selección de PDFs de anverso y reverso
- Reconocimiento y fusión automática del orden de páginas
- Selección de carpeta de salida y apertura rápida
- Generación de PDF con un clic
- Omitir automáticamente páginas en blanco: opción activable, utiliza análisis de proporción de píxeles blancos para detectar e ignorar páginas vacías (incluidas páginas casi blancas del escáner) para mejorar la eficiencia de la unión.

## Uso

<div align="center">
   <img width="400" alt="Captura de pantalla" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. Ve a la [página de Releases](https://github.com/Haookun/PdfSplicer/releases) y descarga el instalador `PdfSplicer.dmg` más reciente.
2. Abre el archivo DMG y arrastra `PdfSplicer.app` a la carpeta de Aplicaciones.
3. Inicia PdfSplicer, selecciona los PDFs de anverso/reverso y la ruta de salida, haz clic en "Iniciar unión".

## Empaquetado y distribución

### Script de empaquetado automático

El proyecto incluye el script automático `build_app.sh` para instalar dependencias, empaquetar la App, generar el DMG y verificar el inicio con un solo comando.

Uso:
```bash
bash build_app.sh
```
- El script instala automáticamente las dependencias de requirements.txt y las herramientas de empaquetado.
- Integra automáticamente el directorio bin (pdftoppm y otras herramientas poppler).
- Tras el empaquetado, verifica si la App se inicia y guarda el log en dist/app_test.log.
- Los artefactos se encuentran en la carpeta dist/ (App) y en la raíz del proyecto (DMG).

Puedes personalizar parámetros o corregir dependencias editando directamente `build_app.sh`.

## Licencia
MIT License

## Solución de problemas

- Si ves "pdftoppm no encontrado" o errores similares:
  1. La app usará primero el directorio bin integrado (ya incluido).
  2. Para instalación manual, ejecuta:
     ```bash
     brew install poppler
     ```
  3. Reinicia la app tras la instalación.

## Repositorio
https://github.com/Haookun/PdfSplicer
