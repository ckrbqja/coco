```markdown
## 1. 본문 (차트 분석 및 매매 기법)

### 진입 조건 및 타점
- 우상향 할때 볼린저 수축 밀착 20선위로 오를때 매수
- 하락할때 볼린저 또는 50선 돌파 매수
- 급락후 시장에서 볼린저 수축하고 있으면 20선 돌파 50선 매수 (또는 120선 돌파할때 추가매수)
- 상승이 강력할곳은 캔들이 크게 나올때 매수 (큰 상승가기 전 {추정: 이평밀집})
- 50선이 우상향 구역에 캔들이 50선 아래있을때 매수
- 50선 매매 : 캔들이 50선으로 하락할때 저점에 매수
- 전고점 뚫고 쌍바닥 무조건 매수
- 하락 볼린저 하단 매수
- 상방 돌파 매수
- 매수는 가능한 볼린저 수축할때 매매한다

### 추세 및 이평선 매매법
- 하락후 이평이 나올때 20선이 방향을 알려준다
- 상승장일때 이평이 우상향 하고있을때
- 하락장일때 이평이 하향 하고있다
- 이 그림이 나올때 먼저가서 400선 매매 한다
- 상승후 눌림은 볼린져 쌍바닥 50선돌파
- 400선 돌파 - 전고점이 지지선 될때
- Point 진입하고 50선이 하락한다면 꽝
- 50선이 우상향 하려할때 진입하여야 한다 매수
- 400선 매매, 200선 매매
- 400선이 스마일 패턴으로 상승할때 400매매후 50선이 400선을 돌파 한걸 상승추세이다

### 시간봉 확인
- 매수는 3분봉 확인후 1분봉으로 본다


## 2. AI 답변 및 단계별 시각화 가이드 (Response & Rendering Guide)

(1) 기본 답변 방식
- 답변 순서 템플릿:
  - (a) 시장상태/추세 요약: 우상향 구역, 급락 후 시장, 스마일 패턴 등 판별
  - (b) 핵심 근거: 50선, 400선, 20선, 볼린저 수축 밀착, 전고점 지지 등
  - (c) 진입 타점: 캔들이 50선 아래에서 저점을 형성할 때, 400선/50선 돌파할 때, 전고점 뚫고 쌍바닥 형성할 때
  - (d) 무효화 조건: 진입 후 50선이 하락할 경우 (꽝)
  - (e) 손절: 50선 우상향 실패 및 이탈 시
  - (f) 1차/2차 익절: 볼린저 상단 도달 전후 추세 유지 확인
  - (g) 리스크/주의사항: 3분봉 확인 후 1분봉으로 세밀한 타점을 잡을 것
- 표현 원칙: 
  - 섹션 1의 용어(우상향 구역, 꽝, 추가매수 등)를 그대로 사용하며, 노트에 없는 추가 보조지표(RSI, MACD 등)는 언급하지 않는다.

(2) 1단계 (빠른 시각화): ASCII 그래프 규칙
- 캔들의 흐름과 50선, 400선의 위치, 진입 타점을 텍스트 기호로 표현한다.
- 진입 위치는 `^` (매수)로 표기하고, 이평선 흐름은 `~` 또는 `-`로 표기한다.

```text
[50선 매매 & 400선 스마일 패턴 예시]

Price
  |               / 캔들 상승 (상방 돌파)
  |      \      /
  |       \____/  <-- 전고점 지지 / 400선 매매 
  |     ^  
  |   매수 (캔들이 50선 아래 하락 시 저점)
  | 
  |~~~~~~~~~~~~~~~~~~~ 50선 (우상향 하려할때 진입)
  |
  |------------------- 400선 (스마일 패턴 상승)
  +-------------------------------------------- Time
```

(3) 2단계 (정밀 시각화): 파이썬 렌더링 또는 외부 실제 차트 첨부
- A) 파이썬 `mplfinance` 가상 렌더링 지침:
  - 캔들 타입: `candle`
  - 봉 개수: 약 100봉 내외 (스마일 패턴 곡선이 잘 보이도록 구성)
  - 거래량 표시: 제외 (False)
  - 이평선 기간: MA20, MA50, MA200, MA400 (노트에 언급된 선 위주로 구성)
  - 진입 마커: 캔들이 50선 아래에서 지지받고 우상향하려는 순간 `^` 마커 표시
- B) 웹 검색 지침: "주식 차트 50선 눌림목 반등", "400선 스마일 패턴 돌파 차트" 등의 키워드로 가장 유사한 사례 1장 첨부

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf

# 가상 데이터 생성 (50선 우상향 구역 및 스마일 패턴 모사)
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=100)
close = np.linspace(100, 150, 100) + np.random.randn(100) * 3
# 스마일 형태 굴곡 생성
close[30:70] = close[30:70] - np.linspace(0, 15, 40)
close[70:] = close[70:] + np.linspace(0, 20, 30)

df = pd.DataFrame({'Close': close}, index=dates)
df['Open'] = df['Close'] + np.random.randn(100)
df['High'] = df[['Open', 'Close']].max(axis=1) + np.random.rand(100) * 2
df['Low'] = df[['Open', 'Close']].min(axis=1) - np.random.rand(100) * 2

# 이동평균선 임의 설정 (패턴 시각화를 위해 기간 조정)
df['MA20'] = df['Close'].rolling(window=5).mean()
df['MA50'] = df['Close'].rolling(window=15).mean()
df['MA400'] = df['Close'].rolling(window=40).mean()

# 50선 우상향 구역에서 캔들이 50선 아래에 있을 때 매수 타점 마커
buy_markers = [np.nan] * len(df)
# 60번째 봉 부근에서 매수 타점 가정
buy_markers[60] = df['Low'].iloc[60] - 5

apds = [
    mpf.make_addplot(df['MA20'], color='orange', width=1.0),
    mpf.make_addplot(df['MA50'], color='blue', width=1.5),
    mpf.make_addplot(df['MA400'], color='red', width=1.5),
    mpf.make_addplot(buy_markers, type='scatter', markersize=100, marker='^', color='green')
]

mpf.plot(df, type='candle', addplot=apds, style='charles', 
         title="MA50 Dip Buy & MA400 Smile Pattern", volume=False)
```


## 3. 추출된 용어 사전 (JSON 포맷)