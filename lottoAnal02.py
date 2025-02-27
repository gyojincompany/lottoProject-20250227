import pandas as pd
import matplotlib.pyplot as plt
import collections
import pymysql

conn = pymysql.connect(host="localhost", user="root", password="12345", db="lottodb")

sql = f"SELECT * FROM lotto_tbl"

cur = conn.cursor()
cur.execute(sql)
result = cur.fetchall()

cur.close()
conn.close()

lottoDf = pd.DataFrame(result, columns=['추첨회차','추첨일','당첨번호1','당첨번호2','당첨번호3','당첨번호4','당첨번호5','당첨번호6','보너스번호'])
print(lottoDf)

lottoDf['추첨일'] = pd.to_datetime(lottoDf['추첨일'])  # 추첨일을 pandas의 날짜타입으로 변환
lottoDf['추첨월'] = lottoDf['추첨일'].dt.month  # 월만 추출
print(lottoDf)

lotto_month_02 = lottoDf[lottoDf['추첨월'] == 3]  # 2월에 출현 했던 당첨 번호 데이터만 추출
print(lotto_month_02)

lottoMonthAllList = list(lotto_month_02['당첨번호1'])+list(lotto_month_02['당첨번호2'])+list(lotto_month_02['당첨번호3'])+list(lotto_month_02['당첨번호4'])+list(lotto_month_02['당첨번호5'])+list(lotto_month_02['당첨번호6'])+list(lotto_month_02['보너스번호'])
print(lottoMonthAllList)
lottoMonthCount = collections.Counter(lottoMonthAllList)  # 2월에 출현한 1~45 번호의 각 빈도수
print(lottoMonthCount)

lottoSeries = pd.Series(lottoMonthCount)
lottoSeries = lottoSeries.sort_values(ascending=False)  # 빈도수의 내림차순으로 정렬
lottoSeries = lottoSeries.head(10)  # 빈도수가 높은 순으로 top 10개만 추출
lottoSeries = lottoSeries.sort_index()

lottoSeries.plot(figsize=(10,10), kind='barh', grid=True, title="Lotto Data Graph")
plt.show()