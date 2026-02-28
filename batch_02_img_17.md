## 1. 본문 (차트 분석 및 매매 기법)

### 이동평균선(이평선) 매매
- 50선 매매: 안착후 5, 10, 20 이평이 우상향 & 밀릴때 매수 (하락장, 상승초입장, 횡보장 무관용)
- 20선 돌파시 매수 (눌림에 사용)
- 400선 매매
- 우상향으로 상승할때 장기이평선으로 지지받을때 매수
- 전고점이 지지선으로 될때 함께보면 좋다

### 시간대 및 단기 캔들 매매
- 09 장시작 1분봉 양봉이 나오면 2번째 양봉에 진입
- 스퀴즈구간에서 단타를 친다
- 스퀴즈구간에서 거래량이 나오는구간에서 눌림받고 하락자리 매수

### 볼린저 밴드 매매
- 볼린저 매매: 볼린저 하단 타격후 매수는 볼린저 안으로 들어온 상승 장악형 또는 아래꼬리 (전고점_전저점 지지)
- 볼린저 쌍바닥 칠때 볼린저 하단 타격 2번째 하단 타격시 진입

### 보조지표 및 거래량 확인
- 거래량 확인 1차, 2차, 3차 상승
- RSI 1시간봉 과매도권에 매수

### 하락장 대응
- 하락장에 아래꼬리 달릴때 매수 -> 후 50선 매매

## 2. AI 답변 및 단계별 시각화 가이드 (Response & Rendering Guide)

(1) 기본 답변 방식
- 답변 순서 템플릿:
  - (a) 시장상태/추세 요약: 우상향, 하락장, 횡보장, 스퀴즈구간 등 노트에 명시된 시장 상태 식별
  - (b) 핵심 근거: 5, 10, 20, 50, 400 이평선, 볼린저 밴드(하단), RSI(과매도권), 1분봉, 거래량 중 노트에 존재하는 조건 매칭
  - (c) 진입 타점: 이평선 밀릴때, 20선 돌파시, 09시 2번째 양봉, 볼린저 상승 장악형/아래꼬리, 2번째 하단 타격시 등 원문 조건 충족 시점 명시
  - (d) 무효화 조건: 전고점 지지 이탈, 이평선 우상향 실패 등 원문을 바탕으로 한 추론(노트에 명시된 지지선 이탈 시)
  - (e) 손절: 타격한 볼린저 하단 이탈 또는 지지선(장기이평, 50선) 이탈 시 (노트 맥락 적용)
  - (f) 1차/2차 익절: 1차, 2차, 3차 상승 파동 구간 또는 거래량 터지는 구간
  - (g) 리스크/주의사항: 스퀴즈 구간에서의 단타 리스크, 하락장 대응 시 아래꼬리 필수 확인 등
- 표현 원칙:
  - '안착', '밀릴때', '타격', '상승 장악형', '과매도권' 등 섹션 1의 표현을 그대로 사용.
  - 노트에 없는 MACD, 일목균형표 등의 지표는 절대 추가하지 않는다.

(2) 1단계 (빠른 시각화): ASCII 그래프 규칙
- 캔들 흐름은 `[]`, `|`, `+`, `-` 등의 기호로 표현.
- 이평선은 `~~~` (50선), `---` (20선), 볼린저 밴드는 `===` (상/하단)으로 매핑하여 표기.
- 진입 타점은 `^ (Buy)` 기호로 캔들 하단에 표기.
- 예시 ASCII 그래프 (볼린저 하단 타격 후 상승 장악형 진입 패턴):
```text
[Bollinger Bands Setup]

Upper BB  =========================================
            |
Candles    [ ]       |       | (Buy)
            |       [ ]     [ ]
                    _|_     _|_  <- 상승 장악형 / 아래꼬리
                     |
Lower BB  =========================================
                     ^
                   타격 (1차/2차)
```

(3) 2단계 (정밀 시각화): 파이썬 렌더링 또는 외부 실제 차트 첨부
- 상세 시각화 요청 시, 파이썬 코드로 가상 차트를 생성하거나 웹 검색을 통해 유사한 차트를 제공한다.
- 차트 렌더링 구체 세팅 값:
  - 캔들 타입: candle 고정
  - 봉 개수: 30~50봉 (단기 패턴 식별용)
  - 거래량 표시 여부: True (노트의 "거래량 확인 1, 2, 3차" 반영)
  - 이평선 기간(mav): (5, 10, 20, 50, 400) 노트에 명시된 선 위주로 세팅
  - 보조지표: Bollinger Bands (20, 2), RSI (14, 1시간봉 기준 과매도 표기용)
  - 마커 위치: "2번째 하단 타격", "50선 밀릴때", "09 장시작 2번째 양봉" 위치에 화살표 및 텍스트 라벨 추가
- 실행 가능한 파이썬 코드 블록 (볼린저 밴드 하단 타격 및 상승 장악형 시뮬레이션):
```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 가상의 주가 데이터 생성 (볼린저 하단 타격 후 상승 장악형 패턴)
np.random.seed(42)
days = 30
close_prices = 1000 + np.cumsum(np.random.randn(days) * 10)
close_prices[20:23] = [980, 960, 995] # 하락 후 상승 장악형 연출
high_prices = close_prices + np.random.rand(days) * 15
low_prices = close_prices - np.random.rand(days) * 15
low_prices[21] = 950 # 아래꼬리 연출 (볼린저 하단 타격)
open_prices = close_prices + np.random.randn(days) * 5
open_prices[21], close_prices[21] = 970, 960 # 음봉
open_prices[22], close_prices[22] = 955, 995 # 양봉 (상승 장악형)

df = pd.DataFrame({'Open': open_prices, 'High': high_prices, 'Low': low_prices, 'Close': close_prices})

# 이평선 및 볼린저 밴드 계산 (간략화된 10일 기준)
df['MA10'] = df['Close'].rolling(window=10).mean()
df['STD'] = df['Close'].rolling(window=10).std()
df['BB_Upper'] = df['MA10'] + (df['STD'] * 2)
df['BB_Lower'] = df['MA10'] - (df['STD'] * 2)

fig, ax = plt.subplots(figsize=(10, 6))

# 캔들차트 그리기
for idx, row in df.iterrows():
    color = 'red' if row['Close'] >= row['Open'] else 'blue'
    ax.plot([idx, idx], [row['Low'], row['High']], color=color, linewidth=1)
    ax.add_patch(plt.Rectangle((idx - 0.3, min(row['Open'], row['Close'])), 0.6, abs(row['Open'] - row['Close']), color=color))

# 이평선 및 볼린저 밴드 플롯
ax.plot(df.index, df['MA10'], label='MA(10)', color='orange', linestyle='--')
ax.plot(df.index, df['BB_Lower'], label='Bollinger Lower', color='purple', alpha=0.5)

# 타점 마커 (노트 표현 그대로)
ax.annotate('볼린저 하단 타격후\n상승 장악형 매수', xy=(22, 955), xytext=(24, 940),
            arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)

plt.title('볼린저 매매: 하단 타격 후 상승 장악형 & 아래꼬리')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```
- 웹 검색 활용 시 키워드 템플릿:
  - "볼린저밴드 하단 타격 상승 장악형 차트"
  - "RSI 과매도권 1시간봉 매수 타점 차트"
  - "50일선 안착 지지선 매수 차트"

## 3. 추출된 용어 사전 (JSON 포맷)