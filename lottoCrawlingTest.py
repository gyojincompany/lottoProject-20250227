import requests
from bs4 import BeautifulSoup

import datetime
import pymysql
import time

# 최신회차번호를 크롤링
url = f"https://dhlottery.co.kr/common.do?method=main"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
recent_count = soup.find("strong",{"id":"lottoDrwNo"}).text.strip()
recent_count = int(recent_count)  # 가장 최신회차 번호

conn = pymysql.connect(host="localhost", user="root", password="12345", db="lottodb")

sql = f"SELECT MAX(count) AS max_count FROM lotto_tbl"

cur = conn.cursor()
cur.execute(sql)
countResult = cur.fetchall()
print(countResult[0][0])
dbCount = int(countResult[0][0])
cur.close()
conn.close()

if recent_count > dbCount:
    for count in range(dbCount+1, recent_count+1):

        lottoCount = count  # 로또 회차
        url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={lottoCount}"

        html = requests.get(url).text

        # print(html)
        soup = BeautifulSoup(html, 'html.parser')

        lottoDate = soup.find('p',{'class':'desc'}).text  # 로또 추첨일
        print(lottoDate)

        lottoDate = datetime.datetime.strptime(lottoDate, "(%Y년 %m월 %d일 추첨)")  # 날짜 문자열->date type 변환
        print(lottoDate)

        lottoNumbers = soup.find('div',{'class':'num win'}).find('p').text.strip().split('\n')
        print(lottoNumbers)

        lottoNumberList = []

        # 문자열인 로또 번호를 정수로 바꾼 후에 list로 변환
        for lottoNum in lottoNumbers:
            # print(lottoNum)
            lottoNum = int(lottoNum)
            # print(lottoNum)
            lottoNumberList.append(lottoNum)

        print(lottoNumberList)

        lottoBonusNumber = soup.find('div',{'class':'num bonus'}).find('p').text.strip()
        print(lottoBonusNumber)
        lottoBonusNumber = int(lottoBonusNumber)
        print(lottoBonusNumber)

        # insert문 구현
        conn = pymysql.connect(host="localhost", user="root", password="12345", db="lottodb")
        # localhost->192.168.0.100, user->guest1, password->12345

        sql = f"insert into lotto_tbl values({lottoCount},'{lottoDate}', {lottoNumberList[0]},{lottoNumberList[1]},{lottoNumberList[2]},{lottoNumberList[3]},{lottoNumberList[4]},{lottoNumberList[5]},{lottoBonusNumber})"

        cur = conn.cursor()
        cur.execute(sql)

        cur.close()
        conn.commit()
        conn.close()

        time.sleep(0.5)