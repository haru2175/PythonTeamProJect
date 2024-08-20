import time # 로딩속도를 sleep()메소드를 활용해 속도를 조절한다.
import json # 파일 json으로 저장하기 위해 임포트를한다.
from bs4 import BeautifulSoup # 페이지의 HTML 소스코드를 파싱하여 필요한 데이터를 추출하는데 사용한다.
from selenium import webdriver
# 설명: selenium은 웹 애플리케이션의 테스트를 자동화하는 도구입니다. webdriver는 Selenium의 핵심 구성 요소 중 하나로, 실제 웹 브라우저를 제어할 수 있게
# 해줍니다.


# Selenium Webdriver를 이용하여 브라우저를 제어합니다. 여기서는 Chrome 브라우저를 사용합니다.
driver = webdriver.Chrome()

# 웹페이지 로딩을 위한 최대 대기 시간을 설정합니다.
wait_time = 10 # 최대 대기 시간

# 암묵적으로 최대 대기 시간을 설정하여, 요소가 로드될 때까지 기다립니다.
driver.implicitly_wait(wait_time)

driver.maximize_window() # 윈도우 창 최대화합니다.

# 크롤링할 네이버 뉴스 카테고리의 이름과 고유 ID를 딕셔너리로 저장합니다.
Urls = {
    "정치": "100",
    "경제": "101",
    "사회": "102",
    "생활/문화": "103",
    "IT/과학": "105",
    "세계": "104"
}

# 모든 카테고리의 기사를 저장할 리스트를 초기화합니다.
all_articles = []

# 각 카테고리를 순회하면서 뉴스를 크롤링합니다.
for Urls_name, Url_id in Urls.items():
    # 해당 카테고리 페이지로 이동합니다.
    driver.get(f'https://news.naver.com/section/{Url_id}') # 정치 --> 경제 -- >사회 --> 생활/문화 ---> IT/과학 ---> 세계

    # 페이지가 완전히 로드될 때까지 대기합니다.
    time.sleep(2)

    # 현재 페이지의 HTML 소스 코드를 가져옵니다.
    html = driver.page_source

    # 가져온 HTML 소스 코드를 파일로 저장합니다.
    filename = 'NaverNews.html'
    htmlfile = open(filename, 'w', encoding='UTF-8')
    print(html, file=htmlfile)
    htmlfile.close()
    print(filename + '파일 생성됨')

    # BeautifulSoup을 사용하여 HTML 소스 코드를 파싱합니다.
    soup = BeautifulSoup(html, 'html.parser')

    # 기사 목록을 가져옵니다. 여기서는 'a.sa_text_title' 클래스의 <a> 태그를 선택합니다.
    articles = soup.select('a.sa_text_title')


    # 각 기사에 대해 정보 추출을 시도합니다.
    for article in articles:
        # 기사 링크를 추출합니다. <a> 태그의 'href' 속성 값을 가져옵니다.
        article_link = article['href']

        # 기사 제목을 추출합니다. <a> 태그 내에서 <strong> 태그로 감싸진 텍스트를 가져옵니다.
        article_title = article.find('strong').get_text()

        # Selenium을 통해 추출한 기사 링크로 이동하여 본문과 이미지를 가져옵니다.
        driver.get(article_link)
        # time.sleep(2)  # 페이지 로딩 대기

        # 로드된 페이지의 HTML 소스 코드를 가져옵니다.
        article_html = driver.page_source

        # 가져온 HTML 소스를 다시 BeautifulSoup을 사용하여 파싱합니다.
        article_soup = BeautifulSoup(article_html, 'html.parser')

        # 언론사 정보를 추출합니다. 'meta[property="og:article:author"]' 메타 태그에서 언론사 이름을 가져옵니다.
        press = article_soup.select_one('meta[property="og:article:author"]')
        press_name = press['content'] if press else '언론사 없음'

        # 기사 본문을 추출합니다. 본문이 위치한 <div> 태그를 선택하여 텍스트를 가져옵니다.
        article_body = article_soup.select_one('#dic_area')  # 본문 영역 선택
        article_body_text = article_body.get_text(strip=True) if article_body else '본문 없음'

        # 기사 내에 포함된 이미지를 추출합니다. 여기서는 'img#img1' 태그를 선택합니다.
        article_images = article_soup.select('#img1')  # 모든 이미지 선택
        image_urls = [img['src'] for img in article_images if 'src' in img.attrs ]  # 이미지 URL 추출

        # 추출한 기사 정보를 딕셔너리 형태로 리스트에 저장합니다.
        all_articles.append({
            '카테고리': Urls_name,
            '언론사': press_name.split("|")[0].strip(), # 언론사 이름이 여러개일 경우 첫 번째 언론사만 저장합니다.
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

# 크롤링한 모든 기사 데이터를 JSON 파일로 저장합니다.
with open('naver_news_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print(f'데이터를 naver_news_data.json 파일로 저장했습니다.')

# 크롤링 작업이 끝난 후 브라우저를 종료합니다.
driver.quit()

