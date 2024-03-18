import requests
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
import urllib.request
import tqdm
from matplotlib import font_manager, rc
from datetime import datetime, timedelta

import matplotlib.dates as mdates



import time
from matplotlib.dates import DateFormatter, HourLocator

#--------폰트 지정
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)



def get_date_list(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.strptime(end_date_str, "%Y%m%d")
    date_list = []

    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    return date_list

def get_aws(date):
    Site = 85
    Dev = 1
    Year = date.year
    Mon = f"{date.month:02d}"
    Day = f"{date.day:02d}"

    aws_url =f'http://203.239.47.148:8080/dspnet.aspx?Site={Site}&Dev={Dev}&Year={Year}&Mon={Mon}&Day={Day}'
    data = urllib.request.urlopen(aws_url)

    df = pd.read_csv(data, header=None)
    df.columns = ['datetime', '온도', '습도', 'X', 'X', 'X', 'rad', 'wd', 'X', 'X', 'X', 'X', 'X', 'ws', '강수', 'maxws', 'bv', 'X']
    drop_cols = [col for col in df.columns if 'X' in col]
    df = df.drop(columns=drop_cols)

    # 0.61078 * np.exp(온도 / (온도 + 233.3) * 17.2694)
    df['SVP'] = 0.61078 * np.exp(df['온도'] / (df['온도'] + 233.3) * 17.2694)

    # svp * (1 - 습도 / 100)
    df['VPD'] = df['SVP'] * (1 - df['습도'] / 100)

    return df

def save_aws(start_date_str, end_date_str, output_dir):
    date_list = get_date_list(start_date_str, end_date_str)

    all_filename = f'{start_date_str}_{end_date_str}.csv'
    all_filename = os.path.join(output_dir, all_filename)
    if not os.path.exists(all_filename):
        all_data = pd.DataFrame()
        for date in tqdm.tqdm(date_list):
            each_data = get_aws(date)
            all_data = pd.concat([all_data, each_data])

        all_data.to_csv(all_filename, index=False)
    else:
        all_data = pd.read_csv(all_filename)

    all_data['datetime'] = pd.to_datetime(all_data['datetime'])
    return all_data

def draw_all_line(df, output_dir, start_date_str, end_date_str, value, unit):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(df['datetime'], df[value])
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y%m%d'))
    plt.xticks(rotation=25)
    plt.ylabel(f'{value} ({unit})')
    plt.xlabel('날짜')
    plt.title(f'{start_date_str} ~ {end_date_str} | {value}')
    plt.savefig(os.path.join(output_dir, f'{start_date_str}_{end_date_str}_{value}.png'))

def draw_min_max(df, output_dir, start_date_str, end_date_str):
    group_df = df
    group_df['date'] = group_df['datetime'].dt.date
    min_max = df.groupby('date').agg(max=('온도', 'max'),
                                     min=('온도', 'min')).reset_index()



    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(min_max['date'], min_max['max'])
    ax.plot(min_max['date'], min_max['min'])
    plt.xticks(rotation=25)
    plt.xlabel('날짜')
    plt.ylabel(f'온도 (℃)')
    plt.title(f'{start_date_str} ~ {end_date_str} | 최저 최고 온도')
    plt.savefig(os.path.join(output_dir, f'{start_date_str}_{end_date_str}_최저최고온도.png'))

def draw_min_max_hum(df, output_dir, start_date_str, end_date_str):
    group_df = df
    group_df['date'] = group_df['datetime'].dt.date
    min_max = df.groupby('date').agg(max=('습도', 'max'),
                                     min=('습도', 'min')).reset_index()



    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(min_max['date'], min_max['max'])
    ax.plot(min_max['date'], min_max['min'])
    plt.xticks(rotation=25)
    plt.xlabel('날짜')
    plt.ylabel(f'습도(%)')
    plt.title(f'{start_date_str} ~ {end_date_str} | 최저 최고 습도')
    plt.savefig(os.path.join(output_dir, f'{start_date_str}_{end_date_str}_최저최고습도.png'))

def main():
    start_date_str = "20231030"
    end_date_str = "20231105"
    output_dir = f'./output/{start_date_str}_{end_date_str}'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    df = save_aws(start_date_str, end_date_str, output_dir)
    draw_all_line(df, output_dir, start_date_str, end_date_str, 'SVP','-')
    draw_all_line(df, output_dir, start_date_str, end_date_str, 'VPD', '-')
    draw_all_line(df, output_dir, start_date_str, end_date_str, '온도', "℃")
    draw_all_line(df, output_dir, start_date_str, end_date_str, '습도', '%')
    draw_min_max(df, output_dir, start_date_str, end_date_str)
    draw_min_max_hum(df, output_dir, start_date_str, end_date_str)





if __name__ == '__main__':
    main()