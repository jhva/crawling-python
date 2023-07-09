import csv
import time
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from searchInfo import SearchInfoFun

url = "https://map.kakao.com/"
page = 1  # 처음 초기 페이지번호
page2 = 0

# 크롬 드라이버 경로 설정
chromedriver_path = "/usr/local/bin/chromedriver"

# 크롬 드라이버 서비스 생성
service = Service(chromedriver_path)

# 크롬 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')  # KR 언어 설정
options.add_argument('--no-sandbox')

# 크롬 드라이버 실행
driver = webdriver.Chrome(service=service, options=options)

# 카카오 지도 페이지 열기
driver.get(url)

# 장소 검색
searchloc = input("장소:")
search = driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')
# 검색 버튼 클릭
search.send_keys(searchloc)
driver.find_element(By.XPATH, '//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)

time.sleep(3)

driver.find_element(By.XPATH, '//*[@id="info.main.options"]/li[2]/a').send_keys(Keys.ENTER)

data_list = []

for i in range(0, 34):
    time.sleep(0.2)
    try:
        page2 += 1
        print("======", page, "======")

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.find_element(By.XPATH, f'//*[@id="info.search.page.no{page2}"]').send_keys(Keys.ENTER)
        time.sleep(1)
        searchList = soup.select('.placelist > .PlaceItem')

        for search in searchList:
            temp = []
            search_info_name = search.select('.head_item > .tit_name > .link_name')[0].text
            search_info_sub_name = search.select('.head_item > .subcategory')[0].text
            search_info_review_rating = search.select('.rating > .score > .num')[0].text
            search_info_place = search.select('.addr')[0].text
            search_info_store_number = search.select('.contact > .phone')[0].text

            temp.append(search_info_name)
            temp.append(search_info_sub_name)
            temp.append(search_info_review_rating)
            temp.append(search_info_place)
            temp.append(search_info_store_number)
            data_list.append(temp)

        if page2 % 5 == 0:
            driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
            page2 = 0
        page+=1



    except:
        break

# CSV 파일 작성
file_name = "잠실_석촌_송리단길.csv"
header = ['장소', '분류', '별점', '주소', '상호 번호']

with open(file_name, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for data in data_list:
        row = [str(item) for item in data]  # 각 항목을 문자열로 변환
        writer.writerow(row)

print('====quit====')

# 크롤링 코드 작성 및 실행

# 크롬 드라이버 종료
driver.quit()
