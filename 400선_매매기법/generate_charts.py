#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
400선 매매기법 차트 자동 생성 스크립트
실행하면 모든 패턴의 차트 이미지가 생성되고 MD 파일이 업데이트됩니다.
"""

import pandas as pd
import numpy as np
import mplfinance as mpf
import os
import re

# 설정
CHARTS_DIR = "charts"
MD_FILE = "400선_쌍바닥_매수법.md"

def ensure_dir(directory):
    """디렉토리가 없으면 생성"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_pattern1_double_bottom():
    """
    패턴1: 200선 아래 쌍바닥 매수
    """
    print("생성 중: 패턴1 - 200선 아래 쌍바닥 매수")
    
    dates = pd.date_range('2023-01-01', periods=80)
    np.random.seed(42)
    
    # 기본 가격 흐름: 하락 후 2번의 저점(쌍바닥) 형성 후 상승
    base_price = (np.linspace(5000, 3000, 20).tolist() +
                  np.linspace(3000, 3800, 15).tolist() +
                  np.linspace(3800, 2900, 15).tolist() +
                  np.linspace(2900, 6000, 30).tolist())
    
    data = {
        'Open': base_price + np.random.normal(0, 50, 80),
        'High': base_price + np.random.normal(100, 50, 80),
        'Low': base_price - np.random.normal(100, 50, 80),
        'Close': base_price + np.random.normal(0, 50, 80),
        'Volume': np.random.randint(1000, 5000, 80)
    }
    df = pd.DataFrame(data, index=dates)
    
    # 거래량이 실린 찐상승 시뮬레이션 (쌍바닥 이후)
    df.loc[dates[50:], 'Volume'] = df.loc[dates[50:], 'Volume'] * 3
    
    # 이평선 데이터
    df['MA100'] = df['Close'].rolling(window=5, min_periods=1).mean() + 500
    df['MA200'] = df['Close'].rolling(window=10, min_periods=1).mean() + 800
    df['MA400'] = df['Close'].rolling(window=20, min_periods=1).mean() + 1500
    
    # 매수 타점 마커
    buy_markers = np.full(len(df), np.nan)
    buy_markers[19] = df['Low'].iloc[19] - 200
    buy_markers[49] = df['Low'].iloc[49] - 200
    
    apds = [
        mpf.make_addplot(df['MA100'], color='green', width=1.0, title="100선"),
        mpf.make_addplot(df['MA200'], color='blue', width=1.5, title="200선"),
        mpf.make_addplot(df['MA400'], color='pink', width=2.0, title="400선"),
        mpf.make_addplot(buy_markers, type='scatter', markersize=100, marker='^', color='red')
    ]
    
    output_path = os.path.join(CHARTS_DIR, "pattern1_double_bottom.png")
    mpf.plot(df, type='candle', style='charles', addplot=apds, volume=True,
             title="패턴1: 200선 아래 쌍바닥 매수",
             ylabel='가격', ylabel_lower='거래량',
             savefig=output_path)
    print(f"  ✓ 저장됨: {output_path}")
    
    return output_path

def create_pattern2_pullback_support():
    """
    패턴2: 400선 돌파 후 눌림 지지
    """
    print("생성 중: 패턴2 - 400선 돌파 후 눌림 지지")
    
    dates = pd.date_range('2023-01-01', periods=80)
    np.random.seed(43)
    
    # 400선 돌파 후 눌림 지지 패턴
    base_price = (np.linspace(2000, 3500, 30).tolist() +
                  np.linspace(3500, 3200, 10).tolist() +
                  np.linspace(3200, 5000, 40).tolist())
    
    data = {
        'Open': base_price + np.random.normal(0, 40, 80),
        'High': base_price + np.random.normal(80, 40, 80),
        'Low': base_price - np.random.normal(80, 40, 80),
        'Close': base_price + np.random.normal(0, 40, 80),
        'Volume': np.random.randint(800, 4000, 80)
    }
    df = pd.DataFrame(data, index=dates)
    
    # 400선 근접 시 거래량 증가
    df.loc[dates[28:35], 'Volume'] = df.loc[dates[28:35], 'Volume'] * 2.5
    
    # 이평선
    df['MA100'] = df['Close'].rolling(window=8, min_periods=1).mean() + 300
    df['MA200'] = df['Close'].rolling(window=15, min_periods=1).mean() + 500
    df['MA400'] = df['Close'].rolling(window=25, min_periods=1).mean() + 800
    
    # 매수 타점 (눌림 지지)
    buy_markers = np.full(len(df), np.nan)
    buy_markers[32] = df['Low'].iloc[32] - 200
    
    apds = [
        mpf.make_addplot(df['MA100'], color='green', width=1.0),
        mpf.make_addplot(df['MA200'], color='blue', width=1.5),
        mpf.make_addplot(df['MA400'], color='pink', width=2.0),
        mpf.make_addplot(buy_markers, type='scatter', markersize=100, marker='^', color='red')
    ]
    
    output_path = os.path.join(CHARTS_DIR, "pattern2_pullback_support.png")
    mpf.plot(df, type='candle', style='charles', addplot=apds, volume=True,
             title="패턴2: 400선 돌파 후 눌림 지지 매수",
             ylabel='가격', ylabel_lower='거래량',
             savefig=output_path)
    print(f"  ✓ 저장됨: {output_path}")
    
    return output_path

def create_pattern3_inverse_head_shoulders():
    """
    패턴3: 역헤드앤숄더 (하락 반전 패턴)
    """
    print("생성 중: 패턴3 - 역헤드앤숄더 하락 반전")
    
    dates = pd.date_range('2023-01-01', periods=80)
    np.random.seed(44)
    
    # 역헤드앤숄더: 하락 후 첫 어깨(L), 헤드(H), 두 번째 어깨(R)
    base_price = (np.linspace(6000, 4000, 15).tolist() +  # 첫 어깨
                  np.linspace(4000, 5000, 10).tolist() +  # 반등
                  np.linspace(5000, 3000, 15).tolist() +  # 헤드 (가장 깊음)
                  np.linspace(3000, 4200, 10).tolist() +  # 반등
                  np.linspace(4200, 3500, 10).tolist() +  # 두 번째 어깨
                  np.linspace(3500, 5500, 20).tolist())    # 상승 반전
    
    data = {
        'Open': base_price + np.random.normal(0, 50, 80),
        'High': base_price + np.random.normal(100, 50, 80),
        'Low': base_price - np.random.normal(100, 50, 80),
        'Close': base_price + np.random.normal(0, 50, 80),
        'Volume': np.random.randint(1000, 5000, 80)
    }
    df = pd.DataFrame(data, index=dates)
    
    # 헤드 이후 거래량 증가
    df.loc[dates[40:], 'Volume'] = df.loc[dates[40:], 'Volume'] * 3
    
    # 이평선
    df['MA100'] = df['Close'].rolling(window=8, min_periods=1).mean() + 400
    df['MA200'] = df['Close'].rolling(window=15, min_periods=1).mean() + 700
    df['MA400'] = df['Close'].rolling(window=25, min_periods=1).mean() + 1200
    
    # 매수 타점 (두 번째 어깨 후 상승 시작)
    buy_markers = np.full(len(df), np.nan)
    buy_markers[60] = df['Low'].iloc[60] - 200
    
    apds = [
        mpf.make_addplot(df['MA100'], color='green', width=1.0),
        mpf.make_addplot(df['MA200'], color='blue', width=1.5),
        mpf.make_addplot(df['MA400'], color='pink', width=2.0),
        mpf.make_addplot(buy_markers, type='scatter', markersize=100, marker='^', color='red')
    ]
    
    output_path = os.path.join(CHARTS_DIR, "pattern3_inverse_head_shoulders.png")
    mpf.plot(df, type='candle', style='charles', addplot=apds, volume=True,
             title="패턴3: 역헤드앤숄더 하락 반전 매수",
             ylabel='가격', ylabel_lower='거래량',
             savefig=output_path)
    print(f"  ✓ 저장됨: {output_path}")
    
    return output_path

def create_pattern4_three_teeth():
    """
    패턴4: 이빨 3개 (하락 3파동)
    """
    print("생성 중: 패턴4 - 이빨 3개 하락 3파동")
    
    dates = pd.date_range('2023-01-01', periods=80)
    np.random.seed(45)
    
    # 이빨 3개: 연속 3번 하락 후 반등
    base_price = (np.linspace(7000, 5000, 15).tolist() +  # 첫 번째 하락
                  np.linspace(5000, 5800, 8).tolist() +   # 반등1
                  np.linspace(5800, 3800, 15).tolist() +  # 두 번째 하락
                  np.linspace(3800, 4500, 8).tolist() +   # 반등2
                  np.linspace(4500, 2500, 17).tolist() +  # 세 번째 하락
                  np.linspace(2500, 4000, 17).tolist())    # 최종 반등
    
    data = {
        'Open': base_price + np.random.normal(0, 60, 80),
        'High': base_price + np.random.normal(120, 60, 80),
        'Low': base_price - np.random.normal(120, 60, 80),
        'Close': base_price + np.random.normal(0, 60, 80),
        'Volume': np.random.randint(1000, 5000, 80)
    }
    df = pd.DataFrame(data, index=dates)
    
    # 마지막 저점 후 거래량 폭증
    df.loc[dates[55:], 'Volume'] = df.loc[dates[55:], 'Volume'] * 4
    
    # 이평선
    df['MA100'] = df['Close'].rolling(window=8, min_periods=1).mean() + 500
    df['MA200'] = df['Close'].rolling(window=15, min_periods=1).mean() + 900
    df['MA400'] = df['Close'].rolling(window=25, min_periods=1).mean() + 1500
    
    # 매수 타점 (마지막 저점)
    buy_markers = np.full(len(df), np.nan)
    buy_markers[55] = df['Low'].iloc[55] - 300
    
    apds = [
        mpf.make_addplot(df['MA100'], color='green', width=1.0),
        mpf.make_addplot(df['MA200'], color='blue', width=1.5),
        mpf.make_addplot(df['MA400'], color='pink', width=2.0),
        mpf.make_addplot(buy_markers, type='scatter', markersize=100, marker='^', color='red')
    ]
    
    output_path = os.path.join(CHARTS_DIR, "pattern4_three_teeth.png")
    mpf.plot(df, type='candle', style='charles', addplot=apds, volume=True,
             title="패턴4: 이빨 3개 하락 3파동 후 매수",
             ylabel='가격', ylabel_lower='거래량',
             savefig=output_path)
    print(f"  ✓ 저장됨: {output_path}")
    
    return output_path

def update_markdown(chart_paths):
    """
    MD 파일을 읽어서 차트 이미지 태그 추가
    """
    print("\nMD 파일 업데이트 중...")
    
    if not os.path.exists(MD_FILE):
        print(f"  ✗ MD 파일을 찾을 수 없음: {MD_FILE}")
        return
    
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 패턴별 이미지 추가
    patterns = [
        ("#### 패턴1: 200선 아래 쌍바닥 매수", chart_paths[0]),
        ("#### 패턴2: 400선 돌파 후 눌림 지지", chart_paths[1]),
        ("#### 패턴3: 역헤드앤숄더 (하락 반전 패턴)", chart_paths[2]),
        ("#### 패턴4: 이빨 3개 (하락 3파동)", chart_paths[3]),
    ]
    
    for pattern_title, chart_path in patterns:
        # 해당 패턴 섹션 찾기
        pattern_regex = re.escape(pattern_title)
        
        # 이미 이미지 태그가 있는지 확인
        img_tag = f"\n\n![{pattern_title}]({chart_path})\n"
        
        if pattern_title in content and chart_path not in content:
            # 패턴 타이틀 다음에 ASCII 그래프 코드 블록이 끝나는 지점을 찾음
            pattern_start = content.find(pattern_title)
            if pattern_start != -1:
                # 다음 #### 또는 ### 을 찾음
                next_section = content.find("\n###", pattern_start + 1)
                if next_section == -1:
                    next_section = content.find("\n##", pattern_start + 1)
                
                if next_section != -1:
                    # 해당 패턴 섹션에 이미지 태그 추가
                    insert_pos = next_section
                    content = content[:insert_pos] + img_tag + content[insert_pos:]
                    print(f"  ✓ 이미지 태그 추가됨: {pattern_title}")
    
    with open(MD_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✓ MD 파일 업데이트 완료: {MD_FILE}")

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("  400선 매매기법 차트 자동 생성")
    print("=" * 60)
    print()
    
    # 디렉토리 생성
    ensure_dir(CHARTS_DIR)
    
    # 모든 패턴 차트 생성
    chart_paths = [
        create_pattern1_double_bottom(),
        create_pattern2_pullback_support(),
        create_pattern3_inverse_head_shoulders(),
        create_pattern4_three_teeth()
    ]
    
    # MD 파일 업데이트
    update_markdown(chart_paths)
    
    print()
    print("=" * 60)
    print("  ✓ 모든 작업 완료!")
    print("=" * 60)
    print()
    print(f"생성된 차트: {CHARTS_DIR}/")
    print(f"업데이트된 파일: {MD_FILE}")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("필요한 라이브러리가 설치되어 있는지 확인하세요:")
        print("  pip install pandas numpy mplfinance matplotlib")
