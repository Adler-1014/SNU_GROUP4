import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pandas as pd

def simple_web_crawler(url):
    data_lst = [] #크롤링한 데이터를 리스트에 저장
    response = requests.get(url)
    
    #웹페이지 불러오기 성공
    if response.status_code == 200: 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('td')
        for p in paragraphs:
            data_lst.append(p.text.strip())
    #웹페이지 불러오기 실패
    else:
        print(f'Failed! :( Status code: {response.status_code}')

    return data_lst

data = simple_web_crawler('http://ie.snu.ac.kr/ko/%ED%95%99%EB%B6%80/%EC%9E%AC%ED%95%99%EC%83%9D/%ED%95%99%EC%82%AC%EC%9D%BC%EC%A0%95')

def snu_event(data):
    month_map = {'1월': '01', '2월': '02', '3월': '03', '4월': '04', '5월': '05', '6월': '06',
                 '7월': '07', '8월': '08', '9월': '09', '10월': '10', '11월': '11', '12월': '12'}
    events = []
    current_month = 0
    current_year = 2023  # Assuming the year is known or fixed

    i = 0
    while i < len(data):
        item = data[i]
        if item in month_map:
            current_month = month_map[item]
            i += 1
            continue

        # Check if the item can be a day
        if '(' in item:
            try:
                day = int(item.split('(')[0])
                event = data[i + 1].strip('"')  
                date_str = f"{current_year}{current_month}{day:02}"  # Format YYYYMMDD
                
                #중복되는 이벤트 존재 여부
                existing_event = next((e for e in events if e['Date'] == date_str), None)
                if existing_event:
                    # If event exists, concatenate the new event
                    existing_event['Event'] += ', ' + event
                else:
                    # If event doesn't exist, add as new entry
                    events.append({'Date': date_str, 'Event': event})
                    
                i += 2  # Move to the next relevant entry after the event
            except ValueError:
                # Handle cases where conversion to int fails
                print(f"Skipping invalid day entry: {item}")
                i += 1  # Skip this entry
        else:
            i += 1  # Increment to next item if not processing

    return events


df_events = pd.DataFrame(snu_event(data))
#print(df_events)
#df_events.to_csv('snu_crawling_2023.csv', index=False)