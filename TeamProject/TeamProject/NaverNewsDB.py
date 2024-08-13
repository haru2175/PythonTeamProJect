import sqlite3
import pandas as pd

csv_file = './naver_news_data.csv'
df = pd.read_csv(csv_file)

conn = sqlite3.connect('./../mydatabase.sqlite3')   # 접속 객체
cursor = conn.cursor()  # 커서 객체

# movies 테이블을 생성하는 문장입니다. (필요에 따라 데이터 타입을 지정)
sql = '''
create table if not exists news(
    movieCd integer,
    movieNm text,
    movieNmEn text,
    prdtYear real,
    openDt real,
    typeNm text,
    prdtStatNm text,
    nationAlt text,
    genreAlt text,
    repNationNm text,
    repGenreNm text
)
'''

cursor.execute(sql)

df.to_sql('movies', conn, if_exists='append', index=False)

conn.commit()
conn.close()

print('데이터 베이스 파일에 데이터 추가를 성공하였습니다.')