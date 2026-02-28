## 1. 본문 (차트 분석 및 매매 기법)

### 장대양봉 및 상한가 종목 매매 타점
- 장대양봉이 나온 후 하락바닥에서 400선 아래서 매수한다 (하락돌파 할때)
- 전날 상한가 종목이 다음날 09시 이내 매수, 브이왑 하락 돌파 할때 매수
- 09시 상승이 크게 나온 종목 첫눌림에 매수간다
- 장대양봉 후 큰하락 올때 지지한다

### 브이왑 및 400선 활용 기법
- 브이왑이 위에 있을때 아래 400선이 있다면 지지받을때 매수
- 하락바닥에서 400, 브이왑이 있으면 20선 돌파하면 상승한다 (자주 나온다)
- 차트 표기: 고점(+20%) 형성 후 하락 시 위에 '브이왑', 아래에 '400선 지지선' 형성

### 상승 후 눌림 형성될 때 체크포인트
- ◎ 전저점 지지 3바닥은 좋다
- ◎ 장기이평선 부근인지
- ◎ 20선 하락이 멈추었는지
- ◎ 브이왑 하락 돌파하는지 (20선 상단에 있으면 좋다)

### 눌림목 상세 조건
- ① 볼린저 하단을 밑꼬리가 깨거나 이탈할때
- ② 음봉이 높은 거래량이 나올때
- ③ 1차 100선 부근, 2차 20선, 3차 60선 매수

## 2. AI 답변 및 단계별 시각화 가이드 (Response & Rendering Guide)

(1) 기본 답변 방식
- 답변 순서 템플릿:
  - (a) 시장상태/추세 요약
  - (b) 핵심 근거 (장대양봉/상한가 이후 하락, 브이왑, 400선, 20선 등 노트 명시 조건)
  - (c) 진입 타점 (브이왑 하락 돌파 시, 400선 지지 시, 20선 돌파 시 등)
  - (d) 무효화 조건
  - (e) 손절
  - (f) 1차/2차 익절
  - (g) 리스크/주의사항
- 표현 원칙:
  - '브이왑', '400선', '밑꼬리', '장대양봉' 등 노트에 기재된 원문 용어를 그대로 사용하여 설명할 것.
  - 노트에 언급되지 않은 보조지표(RSI, MACD 등)는 절대 임의로 추가하여 설명하지 말 것.

(2) 1단계 (빠른 시각화): ASCII 그래프 규칙
- 사용자가 기본 설명을 요청할 경우, 텍스트 기호를 활용한 ASCII 차트를 출력한다.
- ASCII 그래프 규칙:
  - 캔들 흐름: 고점(Peak) 형성 후 하락(W자 패턴 또는 급락)하는 모습 표현
  - 주요 선: `===` (브이왑), `---` (400선/100선/20선 등)
  - 진입/매도 마커: `B` (매수/매수구간), `S` (매도)
- 예시 ASCII 그래프 (브이왑 하락 돌파 및 400선 지지 매수 패턴):
```text
[+20% High]
    /\
   /  \
  /    \       VWAP (브이왑)
=====================================
        \      
         \     <- 브이왑 하락 돌파 
          \    
           \   B (매수)
------------------------------------- 400선 지지선
            \ /
             W (지지)
```

(3) 2단계 (정밀 시각화): 파이썬 렌더링 또는 외부 실제 차트 첨부
- 사용자가 "자세히 그려줘", "정확한 차트를 보여줘"라고 요청 시 아래 지침에 따라 처리한다.
- **A) 파이썬 코드 렌더링 지침 및 세팅 값:**
  - 캔들 타입: `candle` 고정
  - 봉 개수: default (80봉)
  - 거래량 표시: True (음봉 시 높은 거래량 조건 확인용)
  - 이평선 기간(mav): 20, 60, 100, 400 (노트에 기재된 선만 포함)
  - 지지/저항선 위치: 하단 400선, 중간 브이왑 라인
  - 진입 마커 위치: 브이왑 라인을 하향 돌파하는 구간 및 400선 지지 구간에 'Buy' 라벨 표기
  - 차트 제목: "장대양봉 후 눌림목 & 브이왑/400선 매매 타점"

```python
import pandas as pd
import numpy as np
import mplfinance as mpf

# 1. 가상의 데이터 생성 (장대양봉 후 하락, 브이왑 이탈 및 400선 지지 후 20선 돌파)
np.random.seed(42)
dates = pd.date_range('2023-10-01', periods=80, freq='D')
open_price = np.linspace(100, 150, 20).tolist() + np.linspace(150, 110, 30).tolist() + np.linspace(110, 130, 30).tolist()
high_price = [p + np.random.uniform(2, 5) for p in open_price]
low_price = [p - np.random.uniform(2, 8) for p in open_price]  # 밑꼬리 생성을 위한 변동성
close_price = [p + np.random.uniform(-3, 3) for p in open_price]
volume = [np.random.randint(1000, 5000) for _ in range(80)]

# 특정 구간(음봉 + 높은 거래량) 시뮬레이션
volume[40] = 9000 
close_price[40] = low_price[40] + 1 

df = pd.DataFrame({'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price, 'Volume': volume}, index=dates)

# 2. 보조지표 설정 (노트 명시 지표)
# 400선(장기이평) 및 브이왑(VWAP - 여기서는 가상의 고정/완만한 선으로 대체)
df['MA20'] = df['Close'].rolling(window=20, min_periods=1).mean()
df['MA400_Mock'] = 105.0 # 400선 지지선 가상 설정
df['VWAP_Mock'] = 125.0  # 브이왑 가상 설정

# 3. 매수 타점 설정 (브이왑 하락 돌파 및 400선 지지 부근)
buy_signals = np.full(len(df), np.nan)
buy_signals[45] = df['Low'].iloc[45] - 5 # 400선 부근 지지 시점

apd = [
    mpf.make_addplot(df['MA20'], color='green', width=1.0, panel=0),
    mpf.make_addplot(df['MA400_Mock'], color='red', width=1.5, panel=0, linestyle='--'),
    mpf.make_addplot(df['VWAP_Mock'], color='blue', width=1.5, panel=0, linestyle='-.'),
    mpf.make_addplot(buy_signals, type='scatter', markersize=100, marker='^', color='magenta', panel=0)
]

# 4. 차트 렌더링
mpf.plot(df, type='candle', volume=True, addplot=apd, style='yahoo',
         title="Bullish Candle Dip & VWAP/400 Support",
         ylabel="Price", ylabel_lower="Volume")
```

- **B) 웹 검색 사용 시 규칙:**
  - 검색 키워드 템플릿: `"VWAP 하향 돌파 매매 기법 차트"`, `"장기 이평선(400일선) 지지 W바닥 차트"`
  - 가장 유사한 차트 1개만 보조 자료로 첨부할 것.

## 3. 추출된 용어 사전 (JSON 포맷)