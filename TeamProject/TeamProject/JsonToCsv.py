import json
import csv

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