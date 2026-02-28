## 1. 본문 (차트 분석 및 매매 기법)

### 시장 상황 및 전제 조건
- 10/1 (약간 상승장일때)

### 진입(매수) 타점 및 조건
- ① 거래량이 나온 고점을 매수 고점 선 긋기
- ② 100, 120선 위에서 매수 (하락 추세일때는 1분봉 사용 아님)
- ⑤ 5선 (20선) 쌍바닥, 3바닥 매수
- ⑥ 볼린저 쌍바닥 매수
- ⑦ 볼린저 수렴할때 20선 안착 매수
- 지지선 2번 확인 매수
- 하락 거래량 시작 -> 400선 지지 -> {추정: 지지 2번 | 쌍바닥} 확인 매수

### 진입 금지 및 주의 조건 (필터링)
- ③ 400선 아래 진입금지
- ⑧ 100선이 하락장에 있을때 (400선 아래 역배열)
- 데드크로스 치고 내려갈때 {추정: 곧 | 롱} 매수하면 안된다 (정배열)
- ★ 역배열에선 무조건 매수 X

### 차트 패턴 및 관찰 지표
- ④ 컵앤핸들
- ※ 우상향 할때 볼린저 수렴 관심가짐
- X. 15분봉 거래량에 장대 양봉 있다

## 2. AI 답변 및 단계별 시각화 가이드 (Response & Rendering Guide)

(1) 기본 답변 방식
- 답변 순서 템플릿을 명시하라:
  - (a) 시장상태/추세 요약: "약간 상승장" 또는 "우상향" 여부 우선 판단.
  - (b) 핵심 근거: 100선/120선 위인지, 400선 위인지 확인. 볼린저 수렴 상태 및 이평선 배열(정배열/역배열) 분석.
  - (c) 진입 타점: '5선/20선 쌍바닥/3바닥', '볼린저 수렴 후 20선 안착', '400선 지지 후 2번 확인' 등 노트에 기재된 조건 충족 시 타점 제시.
  - (d) 무효화 조건: 100선 하락 꺾임, 400선 이탈.
  - (e) 손절: 타점의 기준이 된 지지선(20선, 400선 등) 하향 돌파 시.
  - (f) 1차/2차 익절: 거래량이 터진 이전 '고점 선 그은' 위치를 목표가로 설정.
  - (g) 리스크/주의사항: "400선 아래 진입금지", "역배열 무조건 매수 X", "데드크로스 후 하락 시 매수 금지" 강력 경고.
- 표현 원칙:
  - 섹션 1에 추출된 원문 은어/축약어(예: 안착, 쌍바닥, 장대 양봉 등)를 사용자 설명 시 그대로 활용할 것.
  - 노트에 언급되지 않은 RSI, MACD 등의 보조지표를 덧붙여 설명하지 말 것.

(2) 1단계 (빠른 시각화): ASCII 그래프 규칙
- 사용자가 차트 설명을 요청하면, 텍스트 기호를 활용한 ASCII 그래프를 출력한다.
- ASCII 그래프 규칙:
  - 가격 흐름은 `*` 또는 `+` 기호로 상승/하락/수렴을 표현한다.
  - 이평선: 20선은 `~`, 100/120선은 `=`, 400선은 `_` 기호로 매핑하여 하단에 깐다.
  - 볼린저 밴드: 상단은 `\`, 하단은 `/`를 사용하여 좁아지는 수렴(Squeeze) 형태를 표현한다.
  - 진입/지지 마커: `[Buy]`, `[Support]` 라벨을 사용해 직관적으로 표시한다.
- 예시 ASCII 그래프 (볼린저 수렴 및 20선 안착 매수 패턴):
```text
(Volume High - Resistance) ----------------------------- [고점 선 긋기]
BB Upper \                                   / 
          \        **     (+) [Buy!]        /
           \      *  *   *                 / 
20 MA ~~~~~~\~~~~*~~~~*~*~~~~~~~~~~~~~~~~~/~~~~~
             \  *      *                 / 
BB Lower      \/                        /
================================================ 100/120 MA (지향성: 우상향)
________________________________________________ 400 MA (하단 강력 지지)
```

(3) 2단계 (정밀 시각화): 파이썬 렌더링 또는 외부 실제 차트 첨부
- 사용자가 "자세히 그려줘", "정확한 차트를 보여줘" 요청 시 다음 A나 B를 수행한다.
- A) 파이썬 코드로 "가상의 캔들 차트" 렌더링
  - 캔들 타입: `candle` 고정
  - 봉 개수: 80봉 (default)
  - 거래량 표시 여부: True (고점 거래량 확인 목적)
  - 이평선 기간(mav): (5, 20, 100, 120, 400) 모두 표시
  - 볼린저 밴드: 표시 (수렴 구간 강조)
  - 진입 마커: 볼린저 수렴 구간 내 20선 부근에 '20선 안착 매수' 라벨 표기
  - 차트 제목: "약간 상승장 - 볼린저 수렴 & 20선 안착"
- 실행 가능한 파이썬 코드 블록:
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 가상의 캔들 데이터 생성 (약간 상승장, 수렴 구간 반영)
np.random.seed(42)
days = 80
price = np.linspace(100, 120, days) + np.sin(np.linspace(0, 10, days)) * 5
price[50:70] = np.linspace(110, 112, 20) + np.random.normal(0, 0.5, 20) # 볼린저 수렴 & 횡보
price[70:] = price[70:] + np.linspace(0, 10, 10) # 20선 안착 후 상승

data = pd.DataFrame({
    'Close': price,
    'Open': price - np.random.normal(0, 1, days),
    'High': price + np.random.normal(1, 2, days),
    'Low': price - np.random.normal(1, 2, days),
})

# 2. 이동평균선 계산 (노트에 명시된 선들)
data['MA5'] = data['Close'].rolling(window=5).mean()
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA100'] = data['Close'].rolling(window=20, min_periods=1).mean() * 0.9 # 시각화를 위한 100/120선 대용 데이터
data['MA400'] = data['Close'].rolling(window=20, min_periods=1).mean() * 0.8 # 시각화를 위한 400선 대용 데이터

# 볼린저 밴드 계산
data['STD'] = data['Close'].rolling(window=20).std()
data['BB_Upper'] = data['MA20'] + (data['STD'] * 2)
data['BB_Lower'] = data['MA20'] - (data['STD'] * 2)

# 3. 차트 렌더링
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Price (Candle proxy)', color='black', linewidth=1.5)
plt.plot(data['MA20'], label='20 MA', color='orange', linestyle='--')
plt.plot(data['MA100'], label='100/120 MA', color='blue', alpha=0.5)
plt.plot(data['MA400'], label='400 MA (Do Not Enter Below)', color='red', linewidth=2)
plt.plot(data['BB_Upper'], color='gray', linestyle=':', alpha=0.7)
plt.plot(data['BB_Lower'], color='gray', linestyle=':', alpha=0.7)
plt.fill_between(data.index, data['BB_Upper'], data['BB_Lower'], color='gray', alpha=0.1, label='Bollinger Bands')

# 진입 마커 (볼린저 수렴할 때 20선 안착 매수)
plt.annotate('Buy: Settled on 20 MA\n(BB Squeeze)', xy=(65, data['MA20'].iloc[65]), 
             xytext=(50, 125), arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10, color='green')

# 주의 영역 표시 (역배열 매수 X)
plt.annotate('DO NOT BUY HERE\n(Below 400 MA)', xy=(20, 85), 
             xytext=(5, 95), arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10, color='red')

plt.title('Market State: Slight Uptrend / Bollinger Squeeze & 20-MA Support')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```
- B) 외부 실제 차트 검색 첨부 시 규칙
  - 검색 키워드 템플릿: `"Stock chart Bollinger Bands squeeze 20MA bounce"`, `"Crypto chart Cup and Handle pattern"`
  - 사용자가 요구하는 패턴과 이평선 형태가 가장 뚜렷한 이미지 1개만 결과에 첨부할 것.

## 3. 추출된 용어 사전 (JSON 포맷)