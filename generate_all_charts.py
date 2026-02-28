#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 batch_01_img_*.md 파일에서 차트 자동 생성 스크립트
실행하면 모든 파일의 차트가 생성되고 MD 파일이 업데이트됩니다.
"""

import pandas as pd
import numpy as np
import mplfinance as mpf
import os
import re
import glob

# 설정
CHARTS_DIR = "charts"
PATTERN_PREFIX = "pattern"

def ensure_dir(directory):
    """디렉토리가 없으면 생성"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_pattern_name(file_path):
    """
    MD 파일에서 패턴 이름 추출
    첫 번째 ### 헤더 다음에 오는 텍스트를 패턴 이름으로 사용
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 첫 번째 ### 헤더 찾기
        match = re.search(r'^### (.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # ### 헤더가 없으면 첫 번째 ## 헤더 사용
        match = re.search(r'^## (.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        return f"패턴_{os.path.basename(file_path)}"
    
    except Exception as e:
        print(f"  ✗ 파일 읽기 오류: {e}")
        return f"패턴_{os.path.basename(file_path)}"

def create_chart_by_pattern(pattern_index, pattern_name):
    """
    패턴 인덱스에 따라 차트 생성
    """
    print(f"생성 중: 패턴 {pattern_index} - {pattern_name}")
    
    dates = pd.date_range('2023-01-01', periods=80)
    
    # 패턴 인덱스별로 다른 시드 사용하여 다양한 패턴 생성
    np.random.seed(40 + pattern_index)
    
    # 패턴 인덱스에 따른 기본 가격 흐름 설정
    if pattern_index % 4 == 0:
        # 쌍바닥 패턴
        base_price = (np.linspace(5000, 3000, 20).tolist() +
                      np.linspace(3000, 3800, 15).tolist() +
                      np.linspace(3800, 2900, 15).tolist() +
                      np.linspace(2900, 6000, 30).tolist())
        title_suffix = "쌍바닥 매수"
    elif pattern_index % 4 == 1:
        # 눌림 지지 패턴
        base_price = (np.linspace(2000, 3500, 30).tolist() +
                      np.linspace(3500, 3200, 10).tolist() +
                      np.linspace(3200, 5000, 40).tolist())
        title_suffix = "눌림 지지 매수"
    elif pattern_index % 4 == 2:
        # 역헤드앤숄더 패턴
        base_price = (np.linspace(6000, 4000, 15).tolist() +
                      np.linspace(4000, 5000, 10).tolist() +
                      np.linspace(5000, 3000, 15).tolist() +
                      np.linspace(3000, 4200, 10).tolist() +
                      np.linspace(4200, 3500, 10).tolist() +
                      np.linspace(3500, 5500, 20).tolist())
        title_suffix = "역헤드앤숄더 반전"
    else:
        # 이빨 3개 패턴
        base_price = (np.linspace(7000, 5000, 15).tolist() +
                      np.linspace(5000, 5800, 8).tolist() +
                      np.linspace(5800, 3800, 15).tolist() +
                      np.linspace(3800, 4500, 8).tolist() +
                      np.linspace(4500, 2500, 17).tolist() +
                      np.linspace(2500, 4000, 17).tolist())
        title_suffix = "하락 3파동 매수"
    
    data = {
        'Open': base_price + np.random.normal(0, 50, 80),
        'High': base_price + np.random.normal(100, 50, 80),
        'Low': base_price - np.random.normal(100, 50, 80),
        'Close': base_price + np.random.normal(0, 50, 80),
        'Volume': np.random.randint(1000, 5000, 80)
    }
    df = pd.DataFrame(data, index=dates)
    
    # 중간 지점부터 거래량 증가
    df.loc[dates[50:], 'Volume'] = df.loc[dates[50:], 'Volume'] * 3
    
    # 이평선
    df['MA100'] = df['Close'].rolling(window=8, min_periods=1).mean() + 400
    df['MA200'] = df['Close'].rolling(window=15, min_periods=1).mean() + 700
    df['MA400'] = df['Close'].rolling(window=25, min_periods=1).mean() + 1200
    
    # 매수 타점 마커
    buy_markers = np.full(len(df), np.nan)
    if pattern_index % 4 == 0:
        # 쌍바닥 저점
        buy_markers[19] = df['Low'].iloc[19] - 200
        buy_markers[49] = df['Low'].iloc[49] - 200
    elif pattern_index % 4 == 1:
        # 눌림 지지
        buy_markers[32] = df['Low'].iloc[32] - 200
    elif pattern_index % 4 == 2:
        # 역헤드앤숄더 두 번째 어깨
        buy_markers[60] = df['Low'].iloc[60] - 200
    else:
        # 이빨 3개 마지막 저점
        buy_markers[55] = df['Low'].iloc[55] - 300
    
    apds = [
        mpf.make_addplot(df['MA100'], color='green', width=1.0, title="100선"),
        mpf.make_addplot(df['MA200'], color='blue', width=1.5, title="200선"),
        mpf.make_addplot(df['MA400'], color='pink', width=2.0, title="400선"),
        mpf.make_addplot(buy_markers, type='scatter', markersize=100, marker='^', color='red')
    ]
    
    # 차트 파일명: pattern_{인덱스}.png
    chart_filename = f"{PATTERN_PREFIX}_{pattern_index}.png"
    output_path = os.path.join(CHARTS_DIR, chart_filename)
    
    mpf.plot(df, type='candle', style='charles', addplot=apds, volume=True,
             title=f"패턴 {pattern_index}: {pattern_name} - {title_suffix}",
             ylabel='가격', ylabel_lower='거래량',
             savefig=output_path)
    print(f"  ✓ 저장됨: {output_path}")
    
    return output_path

def update_markdown(file_path, chart_path):
    """
    MD 파일에 차트 이미지 태그 추가
    """
    print(f"MD 파일 업데이트 중: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 차트 이미지가 있는지 확인
        if chart_path in content:
            print(f"  ✓ 이미 차트 이미지가 있음")
            return
        
        # 패턴 이름 추출
        pattern_name = extract_pattern_name(file_path)
        
        # 차트 이미지 태그 생성
        img_tag = f"\n\n### 차트 시각화\n\n![{pattern_name}](charts/{os.path.basename(chart_path)})\n\n"
        
        # 첫 번째 ## 헤더 뒤에 차트 추가
        first_header_pos = content.find("\n## ")
        if first_header_pos != -1:
            # 다음 ## 헤더 찾기
            next_header_pos = content.find("\n## ", first_header_pos + 1)
            
            if next_header_pos != -1:
                # 첫 번째 ## 섹션의 끝에 차트 추가
                insert_pos = next_header_pos
                content = content[:insert_pos] + img_tag + content[insert_pos:]
            else:
                # 다음 ## 헤더가 없으면 파일 끝에 추가
                content += img_tag
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ 차트 이미지 추가됨")
    
    except Exception as e:
        print(f"  ✗ MD 파일 업데이트 오류: {e}")

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("  모든 batch_01_img_*.md 파일 차트 자동 생성")
    print("=" * 60)
    print()
    
    # 디렉토리 생성
    ensure_dir(CHARTS_DIR)
    
    # 모든 batch_01_img_*.md 파일 찾기
    pattern_files = sorted(glob.glob("batch_01_img_*.md"))
    
    if not pattern_files:
        print("✗ batch_01_img_*.md 파일을 찾을 수 없습니다.")
        return
    
    print(f"발견된 파일: {len(pattern_files)}개")
    for f in pattern_files:
        print(f"  - {f}")
    print()
    
    # 각 파일에 대해 차트 생성 및 MD 업데이트
    for file_path in pattern_files:
        # 파일 번호 추출 (예: batch_01_img_22.md → 22)
        filename = os.path.basename(file_path)
        match = re.search(r'batch_01_img_(\d+)\.md', filename)
        
        if match:
            pattern_index = int(match.group(1))
        else:
            pattern_index = 0
        
        # 패턴 이름 추출
        pattern_name = extract_pattern_name(file_path)
        
        # 차트 생성
        chart_path = create_chart_by_pattern(pattern_index, pattern_name)
        
        # MD 파일 업데이트
        update_markdown(file_path, chart_path)
        
        print()
    
    print("=" * 60)
    print("  ✓ 모든 작업 완료!")
    print("=" * 60)
    print()
    print(f"생성된 차트: {CHARTS_DIR}/")
    print(f"업데이트된 파일: {len(pattern_files)}개")
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
