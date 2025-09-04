<div align="center">
   <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

# PdfSplicer

Já teve dificuldades ao digitalizar documentos frente e verso e não sabe como unir os PDFs em um só?

PdfSplicer resolve isso! Ferramenta inteligente para macOS, interface gráfica, reconhece automaticamente a ordem das páginas e une em um PDF completo.

## Funcionalidades
- Interface gráfica simples
- Seleção de PDFs frente e verso
- Reconhecimento e união automática da ordem das páginas
- Escolha da pasta de saída e abertura rápida
- Geração de PDF com um clique
- Pular automaticamente páginas em branco: opção ativável, detecta e ignora páginas vazias para maior eficiência.

## Como usar

<div align="center">
   <img width="400" alt="Captura de tela" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. Vá até a [página de Releases](https://github.com/Haookun/PdfSplicer/releases) e baixe o instalador `PdfSplicer.dmg` mais recente.
2. Abra o arquivo DMG e arraste `PdfSplicer.app` para a pasta Aplicativos.
3. Inicie o PdfSplicer, selecione os PDFs frente/verso e o caminho de saída, clique em "Iniciar união".

## Empacotamento e distribuição

### Script de empacotamento automático

O projeto inclui o script automático `build_app.sh` para instalar dependências, empacotar o App, gerar o DMG e verificar o início com um único comando.

Como usar:
```bash
bash build_app.sh
```
- O script instala automaticamente as dependências do requirements.txt e as ferramentas de empacotamento.
- Integra automaticamente o diretório bin (pdftoppm e outras ferramentas poppler).
- Após o empacotamento, verifica se o App inicia e salva o log em dist/app_test.log.
- Os artefatos ficam na pasta dist/ (App) e na raiz do projeto (DMG).

Você pode personalizar parâmetros ou corrigir dependências editando diretamente o `build_app.sh`.

## Licença
MIT License

## Solução de problemas

- Se aparecer "pdftoppm não encontrado" ou erros similares:
  1. O app usará primeiro o diretório bin integrado (já incluído).
  2. Para instalação manual, execute:
     ```bash
     brew install poppler
     ```
  3. Reinicie o app após a instalação.

## Repositório
https://github.com/Haookun/PdfSplicer
