import pandas as pd
import matplotlib.pyplot as plt
import collections
import pymysql

# 시각화 그래프에서 한글 깨짐 방지
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

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

for month in range(1,13):  # 1~12월까지 반복

    lotto_month_02 = lottoDf[lottoDf['추첨월'] == month]  # 2월에 출현 했던 당첨 번호 데이터만 추출
    print(lotto_month_02)

    lottoMonthAllList = list(lotto_month_02['당첨번호1'])+list(lotto_month_02['당첨번호2'])+list(lotto_month_02['당첨번호3'])+list(lotto_month_02['당첨번호4'])+list(lotto_month_02['당첨번호5'])+list(lotto_month_02['당첨번호6'])+list(lotto_month_02['보너스번호'])
    print(lottoMonthAllList)
    lottoMonthCount = collections.Counter(lottoMonthAllList)  # 2월에 출현한 1~45 번호의 각 빈도수
    print(lottoMonthCount)

    lottoSeries = pd.Series(lottoMonthCount)
    lottoSeries = lottoSeries.sort_values(ascending=False)  # 빈도수의 내림차순으로 정렬
    lottoSeries = lottoSeries.head(10)  # 빈도수가 높은 순으로 top 10개만 추출
    lottoSeries = lottoSeries.sort_index()

    plt.subplot(4, 3, month)  # 12개의 칸으로 나눈 그래프 설정
    plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.5)  # 그래프의 여백 설정

    lottoSeries.plot(figsize=(10,10), kind='barh', grid=True, title="월별 최다 출현 로또 당첨 번호")
    plt.title(f"{month}월 최다 출현 번호")  # 각 그래프의 타이틀
    plt.xlabel("출현수")
    plt.ylabel("로또번호")

plt.show()