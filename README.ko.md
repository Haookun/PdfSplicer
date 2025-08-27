
<div align="center">
   <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

# PdfSplicer

양면 문서를 스캔할 때 앞뒤 PDF를 하나로 합치는 방법에 고민한 적 있나요?

PdfSplicer가 해결해드립니다! macOS용 스마트 PDF 병합 도구로, 그래픽 UI와 자동 페이지 순서 인식, 클릭 한 번으로 완성된 PDF를 만듭니다.

## 주요 기능
- 직관적인 그래픽 UI
- 앞면/뒷면 PDF 선택
- 페이지 순서 자동 인식 및 병합
- 출력 폴더 선택 및 빠른 열기
- 원클릭 PDF 생성

## 사용법

<div align="center">
   <img width="400" alt="스크린샷" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. [Release 페이지](https://github.com/Haookun/PdfSplicer/releases)에서 최신 `PdfSplicer.dmg`를 다운로드하세요.
2. DMG 파일을 열고 `PdfSplicer.app`을 응용 프로그램 폴더로 드래그합니다.
3. 앱을 실행하고 앞/뒷면 PDF와 출력 경로를 선택, "병합 시작" 클릭.

## 패키징 및 배포
1. 의존성 설치:
   ```bash
   pip install pyinstaller dmgbuild
   ```
2. 투명 배경의 `app_icon.icns`를 프로젝트 루트에 준비.
3. PyInstaller로 .app 생성:
   ```bash
   pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
   ```
   - `dist/PdfSplicer.app`에 생성됨.
4. `dmg_settings.py`로 DMG 설정 확인.
5. DMG 생성:
   ```bash
   dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
   ```
   - DMG는 프로젝트 루트에 생성됨.
6. DMG를 `release` 폴더로 이동.
7. 사용자는 `PdfSplicer.app`을 응용 프로그램 폴더로 드래그하면 설치 완료.

## 라이선스
MIT License

## 저장소
https://github.com/Haookun/PdfSplicer
