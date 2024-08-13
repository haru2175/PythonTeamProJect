import sqlite3
import pandas as pd

# CSV 파일 경로
csv_file = './data/naver_news_data.csv'

# CSV 파일 읽기 (불필요한 Unnamed 컬럼 제거)
df = pd.read_csv(csv_file)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# SQLite 데이터베이스 연결
conn = sqlite3.connect('./../mynewsdatabase.sqlite3')   # 접속 객체 생성
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
