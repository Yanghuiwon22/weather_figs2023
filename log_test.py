import requests
import pandas as pd
import os
from datetime import date, timedelta
import numpy as np
from matplotlib import pyplot as plt

# from cal import cal_svp, cal_vpd

def cal_svp(temp):
    svp = 0.61078 * np.exp(np.array(temp) / (np.array(temp) + 233.3) * 17.2694)
    return svp

def cal_vpd(svp, hum):
    vpd = np.array(svp)*(1-np.array(hum)/100)
    return vpd



def main():
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if not os.path.exists('output/data_all.csv'):
        # 시작 날짜와 오늘의 날짜 가져오기

        # start_date = date(2023, 10, 16)
        # end_date = date.today() # 오늘까지 데이터 받을 때 사용

        start_date = date(2023, 11, 6)
        end_date = date(2023, 11, 12)

        # 날짜 범위 내의 날짜를 리스트로 저장
        date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        df_list = []

        min_temp_list = []

        for x in date_list:
            year = x.year
            mon = f"{x.month:02d}"
            day = f"{x.day:02d}"

            url = f"http://203.239.47.148:8080/dspnet.aspx?Site=85&Dev=1&Year={year}&Mon={mon}&Day={day}"
            context = requests.get(url).text
            data_sep = context.split("\r\n")

            data_list = [x.split(',')[:-1] for x in data_sep][:-1]

            df = pd.DataFrame(data_list, columns=['시간', '온도(°c)', '습도(%)', 'x', 'x', 'x', '일사(W/m2)',
                                                  '풍향(degree)', 'x', 'x', 'x', 'x', 'x', '풍속(1분평균풍속)(m/s)', '강우(mm)', '최대순간풍속(60초 중 최고값)(m/s)', "배터리전압(V)"])

            df.insert(1, '날짜', df['시간'].str.split(' ').str[0])
            df.insert(2, '시각', df['시간'].str.split(' ').str[1])

            #svp, vpd 계산
            df['SVP'] = cal_svp(df['온도(°c)'].astype(float))
            df['VPD'] = cal_vpd(df['SVP'].astype(float), df['습도(%)'].astype(float))


            df = df.drop('x', axis=1)
            df_list.append(df)

        df_all = pd.concat(df_list)

        df_all.to_csv(f'output/{start_date} - {end_date}.csv', encoding='utf-8-sig', index=False)
if __name__ == '__main__':
    main()
