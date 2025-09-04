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
- 빈 페이지 자동 건너뛰기: 옵션으로 활성화 가능, 내용 분석을 통해 빈 페이지를 자동으로 감지해 효율성 향상.

## 사용법

<div align="center">
   <img width="400" alt="스크린샷" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. [Release 페이지](https://github.com/Haookun/PdfSplicer/releases)에서 최신 `PdfSplicer.dmg`를 다운로드하세요.
2. DMG 파일을 열고 `PdfSplicer.app`을 응용 프로그램 폴더로 드래그합니다.
3. 앱을 실행하고 앞/뒷면 PDF와 출력 경로를 선택, "병합 시작" 클릭.

## 패키징 및 배포

### 자동 패키징 스크립트

프로젝트에는 자동 패키징 스크립트 `build_app.sh`가 포함되어 있어, 한 번에 의존성 설치, 앱 패키징, DMG 생성, 실행 체크를 할 수 있습니다.

사용 방법:
```bash
bash build_app.sh
```
- 스크립트는 requirements.txt와 패키징 관련 의존성을 자동 설치합니다.
- bin 디렉토리(pdftoppm 등 poppler 도구)를 자동으로 포함합니다.
- 패키징 후 앱 실행 가능 여부를 체크하고, 로그를 dist/app_test.log에 저장합니다.
- 산출물은 dist/ 폴더(App)와 프로젝트 루트(DMG)에 생성됩니다.

파라미터나 의존성 수정은 `build_app.sh`를 직접 편집하세요.

## 라이선스
MIT License

## 문제 해결

- "pdftoppm을 찾을 수 없음" 또는 유사 오류 발생 시:
  1. 앱은 먼저 내장 bin 디렉토리(이미 통합)를 사용합니다.
  2. 수동 설치가 필요하다면 다음을 실행:
     ```bash
     brew install poppler
     ```
  3. 설치 후 앱을 재시작하세요.

## 저장소
https://github.com/Haookun/PdfSplicer
