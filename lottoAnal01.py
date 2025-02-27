import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import collections

conn = pymysql.connect(host="localhost", user="root", password="12345", db="lottodb")

sql = f"SELECT * FROM lotto_tbl"

cur = conn.cursor()
cur.execute(sql)
result = cur.fetchall()

cur.close()
conn.close()

print(result)

lottoDf = pd.DataFrame(result, columns=['추첨회차','추첨일','당첨번호1','당첨번호2','당첨번호3','당첨번호4','당첨번호5','당첨번호6','보너스번호'])
print(lottoDf)

lottoNumDf = pd.DataFrame(lottoDf.iloc[0:,2:])  # 번호들만 들어있는 dataFrame 생성

print(lottoNumDf)

lottoAllList = list(lottoNumDf['당첨번호1'])+list(lottoNumDf['당첨번호2'])+list(lottoNumDf['당첨번호3'])+list(lottoNumDf['당첨번호4'])+list(lottoNumDf['당첨번호5'])+list(lottoNumDf['당첨번호6'])+list(lottoNumDf['보너스번호'])
print(lottoAllList)

# for i in range(1,46):
#     count = 0
#     for num in lottoAllList:  # 1160*7개의 원소가 들어 있는 리스트
#         if num == i:
#             count = count + 1
#
#     print(f"{i}번의 출현 빈도수 : {count}")

lottoCountData = collections.Counter(lottoAllList)  # 빈도수 계산 모듈 Counter
print(lottoCountData)

lottoSeries = pd.Series(lottoCountData)  # pandas 의 Series로 변환
lottoSeries = lottoSeries.sort_index()  # 1~45까지 정렬

lottoSeries.plot(figsize=(10,10), kind='barh', grid=True, title="Lotto Data Graph")
plt.show()

