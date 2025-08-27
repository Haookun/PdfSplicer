# PdfSplicer

<div align="center">
  <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

Já teve dificuldades ao digitalizar documentos frente e verso e não sabe como unir os PDFs em um só?

PdfSplicer resolve isso! Ferramenta inteligente para macOS, interface gráfica, reconhece automaticamente a ordem das páginas e une em um PDF completo.

## Funcionalidades
- Interface gráfica simples
- Seleção de PDFs frente e verso
- Reconhecimento e união automática da ordem das páginas
- Escolha da pasta de saída e abertura rápida
- Geração de PDF com um clique

## Como usar
1. Vá até a [página de Releases](https://github.com/Haookun/PdfSplicer/releases) e baixe o instalador `PdfSplicer.dmg` mais recente.
2. Abra o arquivo DMG e arraste `PdfSplicer.app` para a pasta Aplicativos.
3. Inicie o PdfSplicer, selecione os PDFs frente/verso e o caminho de saída, clique em "Iniciar união".

## Empacotamento e distribuição
1. Instale as dependências:
   ```bash
   pip install pyinstaller dmgbuild
   ```
2. Prepare um ícone transparente `.icns` chamado `app_icon.icns` na raiz do projeto.
3. Empacote com PyInstaller:
   ```bash
   pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
   ```
   - Saída em `dist/PdfSplicer.app`.
4. Revise ou edite `dmg_settings.py` para configuração do DMG.
5. Crie o DMG:
   ```bash
   dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
   ```
   - DMG na raiz do projeto ou caminho especificado.
6. Mova o DMG para a pasta `release` para distribuição.
7. O usuário só precisa arrastar `PdfSplicer.app` para Aplicativos para instalar.

## Licença
MIT License

## Repositório
https://github.com/Haookun/PdfSplicer
