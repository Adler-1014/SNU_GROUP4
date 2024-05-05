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

def snu_event(data):
    #regex을 통한 데이터 전처리
    date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")  #YYYY-MM-DD
    event_pattern = re.compile(r'(\d{4})년도')  # Example pattern to extract year from event names if relevant

    events = []
    for entry in data:
        date_info, event_name = entry.split(',', 1)
        date_match = date_pattern.search(date_info)
        event_name = event_name.strip('"')  # Remove quotes from the event name

        if date_match:
            year, month, day = map(int, date_match.groups())
            try:
                single_date = pd.Timestamp(year=year, month=month, day=day)
                events.append({'Date': single_date, 'Event': event_name})
            except ValueError as e:
                print(f"Error parsing date: {e}")
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                continue

    return events


df_events = pd.DataFrame(snu_event(data))
print(data)
# df_events.to_csv('snu_crawling.csv', index=False)