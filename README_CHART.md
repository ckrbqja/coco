# 차트 자동 생성 시스템

## 🚀 전체 차트 한 번에 생성하기

```bash
run_all.bat
```

또는:
```bash
pip install pandas numpy mplfinance matplotlib
python generate_all_charts.py
```

## 📁 폴더 구조

```
coco-rag-data/
├── batch_01_img_*.md          # 원본 MD 파일들
├── generate_all_charts.py     # 전체 차트 생성 스크립트
├── run_all.bat                # 윈도우 실행 파일
├── 400선_매매기법/            # 개별 패턴 폴더
│   ├── generate_charts.py     # 개별 차트 생성 스크립트
│   └── run.bat                # 윈도우 실행 파일
└── charts/                    # 생성된 차트 이미지들 (자동 생성)
    ├── pattern_22.png
    ├── pattern_23.png
    ├── pattern_24.png
    └── pattern_25.png
```

## 📊 자동 생성 기능

### 전체 모드
- `run_all.bat` 실행 시 모든 `batch_01_img_*.md` 파일 자동 스캔
- 각 파일에서 패턴 이름 자동 추출
- 파일 번호별 차트 자동 생성
- MD 파일에 차트 이미지 자동 삽입

### 개별 모드
- `400선_매매기법/run.bat` 실행 시 해당 폴더의 차트만 생성

## 📋 사전 준비

### 1. 파이썬 설치
```bash
python --version
```

### 2. 라이브러리 설치
```bash
pip install pandas numpy mplfinance matplotlib
```

## 🎯 자동 감지 패턴

스크립트는 MD 파일에서 첫 번째 `###` 헤더를 읽어 패턴 이름을 추출합니다:

```markdown
### 3분봉 하락장 및 횡보장 진입 조건
```

이 경우 패턴 이름은 `3분봉 하락장 및 횡보장 진입 조건`이 됩니다.

## 📝 생성되는 파일

### 차트 이미지
- `pattern_22.png` - batch_01_img_22.md
- `pattern_23.png` - batch_01_img_23.md
- `pattern_24.png` - batch_01_img_24.md
- `pattern_25.png` - batch_01_img_25.md

### 업데이트되는 파일
- 각 `batch_01_img_*.md` 파일에 차트 이미지 자동 추가

## 🔧 사용 방법

### 전체 파일 한 번에 처리
```bash
cd coco-rag-data
run_all.bat
```

### 특정 파일만 처리 (수동)
```bash
cd coco-rag-data
python generate_all_charts.py
```

## 📊 패턴 타입

스크립트는 파일 번호를 기준으로 4가지 패턴을 자동 생성합니다:

1. **패턴 0, 4, 8...**: 쌍바닥 매수
2. **패턴 1, 5, 9...**: 눌림 지지 매수
3. **패턴 2, 6, 10...**: 역헤드앤숄더 반전
4. **패턴 3, 7, 11...**: 하락 3파동 매수

## 🎨 차트 스타일

- 캔들 차트 (Candlestick)
- 거래량 표시 (Volume)
- 3개 이평선 (100선, 200선, 400선)
- 매수 타점 마커 (빨간색 삼각형)

## 📌 주의사항

- 모든 차트는 가상 데이터로 생성된 예시입니다
- 실제 매매 시에는 실제 차트 분석이 필요합니다
- 손절/익절 전략을 함께 고려하세요
