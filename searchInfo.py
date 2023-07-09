import csv
import time

from bs4 import BeautifulSoup


def SearchInfoFun(driver):
    print(driver, "134134134")
    html = driver
    soup = BeautifulSoup(html, 'html-parser')
    searchList = soup.select('.placelist > .PlaceItem')
    count = 1
    for search in searchList:
        temp = []
        search_info_name = search.select('.head_item > .tit_name > .link_name')
        search_info_sub_name = search.select('.head_item > .tit_name > .subcategory')
        search_info_review_rating = search.select('.rating > .score > .num')[0].text
        search_info_place = search.select('.addr')[0].text
        search_info_store_number = search.select('.contact > .phone')
        # search_info_store_time=search.select()
        temp.append(search_info_place)
        temp.append(search_info_store_number)
        temp.append(search_info_review_rating)
        temp.append(search_info_sub_name)
        temp.append(search_info_name)

        f = open("잠실/석촌(송리단길)" + '.csv', "w", encoding="utf-8-sig", newline="")
        writercsv = csv.writer(f)
        header = ['장소', '분류', '평점', '주소', '상호 번호']
        writercsv.writerow(header)
        for i in list:
            writercsv.writerow(i)
