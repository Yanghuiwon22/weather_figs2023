import datetime

import requests
import pandas as pd
import os
from datetime import date, timedelta, datetime
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
        start_date = date(2023, 11, 26)
        end_date = date(2024, 1, 8)

        print(f'start_date = {start_date}')
        print(f'end_date = {end_date}')

        # 날짜 범위 내의 날짜를 리스트로 저장
        date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        day_list = sorted(set(f'{day.year}-{day.month}' for day in date_list))

        print(day_list)

        df_all = pd.DataFrame()

        for data in day_list:
            year = data.split('-')[0]
            mon = int(data.split('-')[1])

            url = f"https://raw.githubusercontent.com/EthanSeok/JBNU_AWS/main/output/{year}_{mon:02d}.csv"
            response = urllib.request.urlopen(url)
            df = pd.read_csv(response)

            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df_all = pd.concat([df_all, df], axis=0)

        #
        # print(df_all)
        #
        # # 필요한 날짜에 해당하는 데이터프레임 추출
        df = df_all[df_all['Timestamp'].dt.date.between(start_date,end_date)].reset_index()
        df = df.drop(labels='index', axis=1)

        # df['Timestamp'] = datetime.strftime('%Y-%m-%d')
        df.insert(1, 'Date', df['Timestamp'].astype(str).str.split(' ').str[0])
        df.insert(2, 'Time', df['Timestamp'].astype(str).str.split(' ').str[1])

    #
        # svp, vpd 계산
        df['SVP'] = cal_svp(df['Temp'].astype(float))
        df['VPD'] = cal_vpd(df['SVP'].astype(float), df['Humid'].astype(float))

        df.to_csv(f'set_greenhouse_data/output/{start_date}_{end_date}.csv', encoding='utf-8-sig', index=False)

if __name__ == '__main__':
    main()

