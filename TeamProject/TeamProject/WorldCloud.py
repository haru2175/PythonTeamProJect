from collections import Counter  # 단어의 빈도를 계산하기 위해 Counter를 임포트
from wordcloud import WordCloud  # 워드 클라우드를 생성하기 위해 WordCloud 모듈을 임포트
import matplotlib.pyplot as plt  # 생성된 워드 클라우드를 시각화하기 위해 matplotlib를 임포트
import json  # JSON 파일을 읽기 위해 json 모듈을 임포트
from konlpy.tag import Okt  # 한국어 형태소 분석을 위해 Okt 클래스를 임포트
import os  # 자바 환경 설정을 위해 os 모듈을 임포트
import numpy as np  # 마스크 이미지를 배열로 변환하기 위해 numpy를 임포트
from PIL import Image  # 이미지를 열기 위해 PIL의 Image 클래스를 임포트
from wordcloud import ImageColorGenerator  # 마스크 이미지의 색상을 가져오기 위해 ImageColorGenerator를 임포트

# 자바 환경 설정
javahome = 'JAVA_HOME'  # 자바 홈 환경 변수를 설정하기 위해 변수 정의
os.environ[javahome] = r'C:\Program Files\Java\jdk-12.0.1\bin\server'  # 자바 JDK의 경로를 자바 홈으로 설정
# os.environ[javahome] = r'C:\Program Files\Java\jdk-12.0.2\bin\server'  # 자바 JDK의 경로를 자바 홈으로 설정

# JSON 파일 경로

json_file = '../naver_news_data.json' # 분석할 뉴스 데이터가 저장된 JSON 파일의 경로를 변수에 저장

# JSON 파일 읽기
with open(json_file, 'r', encoding='utf-8') as f:  # JSON 파일을 읽기 모드로 열고, UTF-8로 인코딩하여 파일을 염
    data = json.load(f)  # JSON 파일의 내용을 파이썬의 리스트로 로드

# 모든 기사 본문을 하나의 문자열로 합치기
combined_text = ''  # 모든 기사 본문을 저장할 빈 문자열을 초기화
for article in data:  # JSON 데이터의 각 기사를 순회하며
    combined_text += article['기사 본문'] + ' '  # 각 기사의 본문을 combined_text에 추가하고, 단어 간 공백을 추가

# 형태소 분석기 초기화 # konlpy.tag 로해야지 명사로 추출이 된다.
okt = Okt()  # Okt 객체를 초기화하여 형태소 분석을 수행

# 명사 추출
nouns = okt.nouns(combined_text)  # 전체 기사 본문에서 명사만 추출하여 리스트로 반환

# 두 글자 이상인 단어만 필터링
filtered_words = [word for word in nouns if len(word) >= 2]  # 추출된 명사 중에서 두 글자 이상인 단어만 필터링하여 리스트에 저장

# 단어 빈도 계산
word_counts = Counter(filtered_words)  # 필터링된 단어들의 빈도를 계산하여 Counter 객체에 저장

# 상위 10개의 단어 추출
top_10_words = dict(word_counts.most_common(50))  # 가장 많이 등장한 상위 50개의 단어를 딕셔너리로 변환
print("상위 50개 단어:", top_10_words)  # 상위 50개의 단어와 그 빈도를 출력

# 이미지 경로
file_path = os.getcwd()
mask_image_path = file_path + '/data/SouthKorea2.jpg' # 마스크로 사용할 이미지 파일 경로를 변수에 저장

# 마스크 이미지 로드 및 배열로 변환
mask_image = np.array(Image.open(mask_image_path))  # 마스크 이미지를 열어 numpy 배열로 변환

# 상위 50개 단어로 워드 클라우드 생성
wordcloud = WordCloud(font_path='malgun.ttf',  # 한글 폰트 경로 설정, 이걸 설정 안 하면 글이 깨짐
                      background_color='white',  # 도화지 배경색을 흰색으로 설정
                      width=800,  # 워드 클라우드의 너비 설정
                      height=600,  # 워드 클라우드의 높이 설정
                      mask=mask_image,  # 마스크 이미지 배열을 설정하여 워드 클라우드의 형태를 지정
                      contour_color='white',  # 워드 클라우드의 테두리 색상을 흰색으로 설정
                      contour_width=1,  # 테두리의 두께를 1로 설정
                      colormap='rainbow_r'  # 워드 클라우드의 색상 맵을 무지개 색상으로 설정
                      ).generate_from_frequencies(top_10_words)  # 상위 50개의 단어 빈도를 기반으로 워드 클라우드를 생성

# 워드 클라우드 이미지 표시
plt.figure(figsize=(10, 8))  # 워드 클라우드 이미지를 표시할 때의 크기를 설정 (가로 10인치, 세로 8인치)
plt.imshow(wordcloud, interpolation='bilinear')  # 생성된 워드 클라우드를 화면에 표시, bilinear 보간법을 사용
plt.axis('off')  # 축을 표시하지 않음
# plt.show()  # 설정된 플롯을 화면에 출력

# 워드 클라우드 이미지 저장
file_save_path = '../static/images/wordcloud_top_10_nouns_with_mask.png' # 워드 클라우드 이미지 저장 경로
os.makedirs(os.path.dirname(file_save_path), exist_ok=True) # 디렉토리가 존재하지 않으면 생성
wordcloud.to_file(file_save_path) # 워드 클라우드 이미지를 지정한 경로에 파일로 저장
print(f'워드 클라우드 이미지가 {file_save_path} 파일로 저장되었습니다.') # 저장 완료 메시지 출력
