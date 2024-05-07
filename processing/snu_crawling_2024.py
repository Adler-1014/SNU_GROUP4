import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def simple_web_crawler(url):
    data_lst = [] #크롤링한 데이터를 리스트에 저장
    response = requests.get(url)
    
    #웹페이지 불러오기 성공
    if response.status_code == 200: 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            data_lst.append(p.text.strip())
    #웹페이지 불러오기 실패
    else:
        print(f'Failed! :( Status code: {response.status_code}')

    return data_lst

data = simple_web_crawler('https://www.snu.ac.kr/academics/resources/calendar')
print(data)

def snu_event(data):
    date_pattern = re.compile(r'(\d{2})\((월|화|수|목|금|토|일)\)')
    range_pattern = re.compile(r'(\d{2})\((월|화|수|목|금|토|일)\) ~ (\d{2})\((월|화|수|목|금|토|일)\)')
    current_month = None
    current_year = "2024"
    events = []
    prev_day = 0  # 이전 일을 추적하기 위한 변수
    prev_month = None  # 이전 월을 추적하기 위한 변수

    for item in data:
        if item.endswith('월'):
            current_month = item.strip('월').strip()  # '3월'에서 '3' 추출
        elif date_pattern.search(item) or range_pattern.search(item):
            if current_month is None:
                current_month = "3"  # 월 정보가 없는 경우 3월로 설정
                current_year = "2024"  # 현재 년도의 시작 부분으로 설정

            if range_pattern.search(item):
                start_day, _, end_day, _ = range_pattern.search(item).groups()
                days = range(int(start_day), int(end_day) + 1)
            else:
                day, _ = date_pattern.search(item).groups()
                days = [int(day)]
            
            event_idx = data.index(item) + 1 if data.index(item) + 1 < len(data) else data.index(item)
            event_text = data[event_idx]
            
            for day in days:
                if prev_month is not None and int(day) < prev_day and current_month != prev_month:
                    current_month = str(int(current_month) + 1)  # 현재 월을 다음 달로 업데이트
                prev_day = int(day)  # 현재 일을 이전 일로 업데이트
                prev_month = current_month  # 현재 월을 이전 월로 업데이트
                
                # 월이 누락된 경우 이전 월을 사용하여 날짜를 생성
                if current_month is None:
                    current_month = str(int(current_month) - 1)
                date = f"{current_year}{int(current_month):02d}{int(day):02d}"
                events.append({'Date': date, 'Event': event_text})

    return events


df_events = pd.DataFrame(snu_event(data))
print(df_events)
df_events.to_csv('snu_crawling_2024.csv', index=False)
