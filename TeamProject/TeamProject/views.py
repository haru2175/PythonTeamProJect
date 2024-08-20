# render 함수는 클라이언트의 요청을 처리하여 최종 결과인 HTML 문서를 클라이언트에게 되돌려 주는 역할을 합니다.
import os
import time  # 로딩속도를 sleep()메소드를 활용해 속도를 조절한다.
import json  # 파일 json으로 저장하기 위해 임포트를한다.

from django.http import HttpResponse
from django.shortcuts import render
from selenium.common import WebDriverException, NoSuchElementException

from .models import NaverNews

# Create your views here.

# def NaverNews_list(request):
#     # QueerySet는 데이터 베이스 쿼리의 결과 집합을 의미하는 객체입니다.
#     # 장고에서 QuerySet의 기본 이름은 objects입니다.
#     NaverNewss = NaverNews.objects.all()
#
#     return render(request, 'TeamProject/NaverNews_list.html',{'NaverNewsList' : NaverNewss})
# # end def movie_list

from django.core.paginator import Paginator

def NaverNews_list(request): # request는 http 요청 객체입니다.
    # 요청(request)한 mode, keyword 파라미터를 챙깁니다.
    category = request.GET.get('category', None)
    company = request.GET.get('company', None)
    NewsCategory = NaverNews.objects.values('nCategory').distinct()
    NewsCompany = NaverNews.objects.values('nCompany').distinct()

    if category:
        NaverNewss = NaverNews.objects.filter(nCategory=category)
    else:
        NaverNewss = NaverNews.objects.all()

    if company:
        NaverNewss = NaverNewss.filter(nCompany=company)

    pageSize = 10
    paginator = Paginator(NaverNewss, pageSize)

    pageNumber = request.GET.get('page')  # 사용자가 요청한 페이지 번호
    NaverNewsList = paginator.get_page(pageNumber)
    pageCount = 10
    totalPage = paginator.num_pages

    if pageNumber == None:  # 처음 시작 되었을 때
        pageNumber = 1
        beginPage = 1
        endPage = 10

    else:  # 사용자가 Pagination의 숫자를 눌렀을 때
        print('pageNumber=' + pageNumber)  # 파라미터들은 문자열로 넘어 옵니다.
        pageNumber = int(pageNumber)  # 해당 파라미터를 정수형 숫자로 변경합니다.
        beginPage = (pageNumber - 1) // pageSize * pageSize + 1
        endPage = beginPage + pageCount - 1

        # 끝 페이지가 전체 페이지 번호 보다 큰 경우, 끝페이지를  전체 페이지로 대체합니다.
        totalPage = paginator.num_pages
        if totalPage < endPage:
            endPage = totalPage
    # end if

    has_previous = pageNumber > pageCount
    print('has_previous=' + str(has_previous))

    # 주의) 몫 연산을 위하여 //로 나누어야 합니다.
    has_next = pageNumber < (totalPage // pageCount * pageCount + 1)
    print('has_next=' + str(has_next))

    print('beginPage=' + str(beginPage))
    print('endPage=' + str(endPage))

    # Template(html 문서) 파일에서는 range()를 사용할 수 없습니다.
    # 연산이 이루어 지는 과정에 실수로 바뀌기 때문에 다시 정수로 변환해줍니다.
    page_range = range(int(beginPage), int(endPage) + 1)

    # 페이지로 넘어오는 파라미터 정보
    query_params = request.GET.copy()  # 파라미터 목록의 복사본 만들기

    # page 파라미터를 제거한 다음 쿼리 문자열을 전송하도록 합니다.
    delete_param = 'page'

    if 'page' in query_params:
        del query_params[delete_param]

    # 넘겨진 쿼리 목록의 문자열 집합을 QueryString이라고 부릅니다.
    query_params = query_params.urlencode()  # 복사본을 인코딩 문자열로 변환

    print('query_params=[' + str(query_params) + ']')


    context = {'NaverNewsList': NaverNewsList, 'NewsCategory': NewsCategory, "NewsCompany" : NewsCompany,  'beginPage': beginPage, 'endPage': endPage, 'page_range': page_range, 'has_previous': has_previous, 'has_next': has_next, 'query_params': query_params}

    return render(request, 'TeamProject/NaverNews_list.html', context)
# end def movie_pagination

def NaverNews_view(request):
    idx = request.GET.get('idx', None)
    NaverNewss = NaverNews.objects.filter(nIdx=idx)

    return render(request, 'TeamProject/NaverNews_view.html', {'NaverNews': NaverNewss})

from bs4 import BeautifulSoup  # 페이지의 HTML 소스코드를 파싱하여 필요한 데이터를 추출하는데 사용한다.
from selenium import webdriver
def run_naver_news(request):
    # 설명: selenium은 웹 애플리케이션의 테스트를 자동화하는 도구입니다. webdriver는 Selenium의 핵심 구성 요소 중 하나로, 실제 웹 브라우저를 제어할 수 있게
    # 해줍니다.
    success = False

    try:
        # Selenium Webdriver를 이용하여 브라우저를 제어합니다. 여기서는 Chrome 브라우저를 사용합니다.
        driver = webdriver.Chrome()

        # 웹페이지 로딩을 위한 최대 대기 시간을 설정합니다.
        wait_time = 10  # 최대 대기 시간

        # 암묵적으로 최대 대기 시간을 설정하여, 요소가 로드될 때까지 기다립니다.
        driver.implicitly_wait(wait_time)

        driver.maximize_window()  # 윈도우 창 최대화합니다.

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
            driver.get(f'https://news.naver.com/section/{Url_id}')  # 정치 --> 경제 -- >사회 --> 생활/문화 ---> IT/과학 ---> 세계

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
                image_urls = [img['src'] for img in article_images if 'src' in img.attrs]  # 이미지 URL 추출

                # 추출한 기사 정보를 딕셔너리 형태로 리스트에 저장합니다.
                all_articles.append({
                    '카테고리': Urls_name,
                    '언론사': press_name.split("|")[0].strip(),  # 언론사 이름이 여러개일 경우 첫 번째 언론사만 저장합니다.
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

        success = True

    except (WebDriverException, NoSuchElementException, Exception) as e:
        print(f'오류 발생: {e}')

    finally:
        # 크롤링 작업이 끝난 후 브라우저를 종료합니다.
        driver.quit()

        # 작업 성공 여부를 출력합니다.
        if success:
            print("작업이 성공적으로 완료되었습니다.")
        else:
            print("작업이 실패했습니다.")

    return HttpResponse(success)

import json
import csv
def run_json_to_csv(request):
    success = False

    try:
        # JSON 파일 로드 (예: json 파일의 경로를 'data.json'로 가정)
        with open('naver_news_data.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # CSV 파일 저장 경로 지정
        csv_file_path = './data/naver_news_data.csv'

        # CSV 파일로 저장
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # 헤더 작성
            csv_writer.writerow(['nIdx', 'nCategory', 'nCompany', 'nTitle', 'nContent', 'nLink', 'nImage'])

            # 내용 작성
            for idx, entry in enumerate(data):
                csv_writer.writerow([
                    idx + 1,
                    entry["카테고리"],
                    entry["언론사"],
                    entry["기사 제목"],
                    entry["기사 본문"],
                    entry["기사 링크"],
                    ", ".join(entry["이미지 URLs"])
                ])

        print(f"CSV 파일이 '{csv_file_path}'로 저장되었습니다.")
        success = True

    except (WebDriverException, NoSuchElementException, Exception) as e:
        print(f'오류 발생: {e}')

    finally:
        # 작업 성공 여부를 출력합니다.
        if success:
            print("작업이 성공적으로 완료되었습니다.")
        else:
            print("작업이 실패했습니다.")
    return HttpResponse(success)

import sqlite3
import pandas as pd
def run_csv_naver_news(request):
    NaverNews.objects.all().delete()
    success = False;
    try:
        # CSV 파일 경로
        file_path = os.getcwd()
        csv_file = file_path + '/TeamProject/data/naver_news_data.csv'

        # CSV 파일 읽기 (불필요한 Unnamed 컬럼 제거)
        df = pd.read_csv(csv_file)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # SQLite 데이터베이스 연결
        conn = sqlite3.connect(file_path + '/mynewsdatabase.sqlite3')  # 접속 객체 생성
        cursor = conn.cursor()  # 커서 객체 생성

        # NaverNews 테이블 생성
        sql = '''
        create table if not exists NaverNews(
            nIdx integer primary key autoincrement,
            nCategory text,
            nCompany text,
            nTitle text,
            nContent text,
            nLink text,
            nImage text
        )
        '''
        cursor.execute(sql)

        # DataFrame 데이터를 SQLite 테이블에 삽입
        try:
            df.to_sql('NaverNews', conn, if_exists='append', index=False)
            print('데이터베이스 파일에 데이터 추가를 성공하였습니다.')
        except Exception as e:
            print(f"데이터 삽입 중 오류가 발생했습니다: {e}")

        # 변경사항 커밋 및 연결 종료
        conn.commit()
        conn.close()

        success = True
    except (WebDriverException, NoSuchElementException, Exception) as e:
        print(f'오류 발생: {e}')

    finally:
        # 작업 성공 여부를 출력합니다.
        if success:
            print("작업이 성공적으로 완료되었습니다.")
        else:
            print("작업이 실패했습니다.")
    return HttpResponse(success)


