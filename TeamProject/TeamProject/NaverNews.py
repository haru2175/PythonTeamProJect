import pandas as pd
import numpy as np
import folium
import requests
import time
import json
from bs4 import BeautifulSoup

# pip install tqdm : progressBar 구현
from tqdm.notebook import tqdm
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# jupyter nbconvert --to script coffeeStore.ipynb

# chrome_options = webdriver.ChromeOptions() # 크롬 브라우저 옵션
# drive_path = 'chromedriver.exe' # 다운로드 받은 드라이버 파일
# myservice = Service(drive_path) # 드라이버 제어를 위한 서비스 객체
driver = webdriver.Chrome()
wait_time = 10 # 최대 대기 시간
driver.implicitly_wait(wait_time)
driver.maximize_window() # 윈도우 창 최대화

Urls = {
    "정치": "100",
    "경제": "101",
    "사회": "102",
    "생활/문화": "103",
    "IT/과학": "105",
    "세계": "104"
}
# 모든 카테고리의 기사를 저장할 리스트
all_articles = []

for Urls_name, Url_id in Urls.items():
    # driver = webdriver.Chrome()
    driver.get(f'https://news.naver.com/section/{Url_id}') # 정치 --> 경제 -- >사회 --> 세계
    time.sleep(2)

    html = driver.page_source  # 해당 페이지의 소스 코드 반환
    filename = 'NaverNews.html'
    htmlfile = open(filename, 'w', encoding='UTF-8')
    print(html, file=htmlfile)
    htmlfile.close()
    print(filename + '파일 생성됨')
    soup = BeautifulSoup(html, 'html.parser')


    # 기사 목록 가져오기
    articles = soup.select('a.sa_text_title')


    # 기사 정보 추출
    for article in articles:
        article_link = article['href']  # 기사 링크 추출
        article_title = article.find('strong').get_text()  # 기사 제목 추출

        # 기사 링크에 접근하여 본문과 이미지 가져오기
        driver.get(article_link)
        # time.sleep(2)  # 페이지 로딩 대기

        # 본문과 이미지 가져오기
        article_html = driver.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')

        # 언론사 추출
        press = article_soup.select_one('meta[property="og:article:author"]')
        press_name = press['content'] if press else '언론사 없음'

        # 본문 추출
        article_body = article_soup.select_one('#dic_area')  # 본문 영역 선택
        article_body_text = article_body.get_text(strip=True) if article_body else '본문 없음'

        # 이미지 추출
        article_images = article_soup.select('#img1')  # 모든 이미지 선택
        image_urls = [img['src'] for img in article_images if 'src' in img.attrs]  # 이미지 URL 추출

        all_articles.append({
            '카테고리': Urls_name,
            '언론사': press_name.split("|")[0].strip(),
            '기사 링크': article_link,
            '기사 제목': article_title,
            '기사 본문': article_body_text[1:],  # 본문 첫 500자 저장
            '이미지 URLs': image_urls
        })

        print(f'카테고리:{Urls_name}')
        print(f'언론사: {press_name.split("|")[0].strip()}')
        print(f"기사 링크: {article_link}")
        print(f"기사 제목: {article_title}")
        print(f"기사 본문: {article_body_text[1:]}")  # 본문 첫 500자 출력
        print(f"이미지 URLs: {image_urls}")
        print('-' * 30)

with open('naver_news_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print(f'데이터를 naver_news_data.json 파일로 저장했습니다.')
driver.quit()

