import requests
import pandas as pd
import os
from datetime import date, timedelta
import numpy as np
from matplotlib import pyplot as plt
import urllib.request

# from cal import cal_svp, cal_vpd

def cal_svp(temp):
    svp = 0.61078 * np.exp(np.array(temp) / (np.array(temp) + 233.3) * 17.2694)
    return svp

def cal_vpd(svp, hum):
    vpd = np.array(svp)*(1-np.array(hum)/100)
    return vpd


def cal_gdd(temp):
    gdd = [max(0, value - 5) for value in temp]
    return gdd

def cal_gdd_sum(gdd):
    if np.array(gdd)[-1] is True:
        gdd_sum = np.array(gdd)[-1] + np.array(gdd)
    else:
        gdd_sum = np.array(gdd)
    return gdd_sum

def main():
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if not os.path.exists('output/data_all.csv'):
        # 시작 날짜와 오늘의 날짜 가져오기

        # start_date = date(2023, 10, 16)
        # end_date = date.today() # 오늘까지 데이터 받을 때 사용

        start_date = date(2023, 11, 26)
        end_date = date(2024, 1, 8)

        print(f'start_date = {start_date}')
        print(f'end_date = {end_date}')


        # 날짜 범위 내의 날짜를 리스트로 저장
        date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        df_list = []

        for x in date_list:
            year = x.year
            mon = f"{x.month:02d}"
            day = f"{x.day:02d}"

            url = f"https://raw.githubusercontent.com/EthanSeok/JBNU_AWS/main/output/{year}_{mon}.csv"

            response = urllib.request.urlopen(url)
            df = pd.read_csv(response)
        #
        #
        #     df.insert(1, '날짜', df['시간'].str.split(' ').str[0])
        #     df.insert(2, '시각', df['시간'].str.split(' ').str[1])
        #
        #     # svp, vpd 계산
        #     df['SVP'] = cal_svp(df['온도(°c)'].astype(float))
        #     df['VPD'] = cal_vpd(df['SVP'].astype(float), df['습도(%)'].astype(float))
        #     df['GDD'] = cal_gdd(df['온도(°c)'].astype(float))
        #     # df['GDD_sum'] = cal_gdd_sum(df['GDD'].astype(float).tolist())
        #     df_list.append(df)
        #
        #
        # df_all = pd.concat(df_list)


        #
        print(df)
        df.to_csv(f'output/{start_date} - {end_date}.csv', encoding='utf-8-sig', index=False)
if __name__ == '__main__':
    main()

