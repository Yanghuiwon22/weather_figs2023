import os
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
import numpy as np
from matplotlib import font_manager, rc

# CSV 파일 읽기
start_day = '2023-11-13'
end_day = '2023-11-19'

df = pd.read_csv(f'output/{start_day} - {end_day}.csv')
df['시간'] = pd.to_datetime(df['시간'])  # 시간 열을 datetime 형식으로 변환

# font_path = "C:/Windows/Fonts/NGULIM.TTF"
# font = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font)

def figs(df,output_dir, value):
    date = df['시간']
    x = date
    y = df[value]
    x_step = len(x) // 7  # X 축에 표시할 날짜 수를 설정 (여기서는 7개)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y)

    date_format = DateFormatter("%Y-%m-%d")  # 원하는 날짜와 시간 형식 지정
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(plt.MaxNLocator(7))  # X 축에 표시할 눈금 수 조절

    plt.title(f'{value}_graph')

    if value == '온도(°c)':
        plt.yticks(np.arange(0, 25, 5))
        plt.axhline(y=5,color='lightgray', linestyle='--', linewidth=2)
        # plt.text(0,5, 'temp')
    elif value == '습도(%)':
        plt.yticks(np.arange(0, 101, 10))

    ax.set_xlim(pd.to_datetime(start_day), pd.to_datetime('2023-11-19'))
    plt.savefig(f'{output_dir}/{start_day}_{end_day}_{value}.png', dpi=300, bbox_inches='tight')  # 파일명, 해상도 및 여백 설정

    plt.show()

def figs_2(df,output_dir, value1, value2):
    date = df['시간']
    x = date
    y1 = df[value1]
    y2 = df[value2]

    x_step = len(x) // 7  # X 축에 표시할 날짜 수를 설정 (여기서는 7개)

    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax2 = ax1.twinx()

    line1 = ax1.plot(date, y1, color='blue', label = '온도(°c)')
    line2 = ax2.plot(date, y2, color='orange', label = '습도(%)')


    date_format = DateFormatter("%Y-%m-%d")  # 원하는 날짜와 시간 형식 지정
    ax1.xaxis.set_major_formatter(date_format)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(7))  # X 축에 표시할 눈금 수 조절

    ax2.xaxis.set_major_formatter(date_format)
    ax2.xaxis.set_major_locator(plt.MaxNLocator(7))

    title_font = {
        'fontsize': 16,
        'fontweight': 'bold'
    }

    plt.title('temp.&hum._graph', fontdict=title_font, pad=20)
    # plt.title(f'temp.&hum._graph')
    ax1.set_ylabel('온도(°c)')
    ax2.set_ylabel('습도(%)')

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')

    ax1.set_xlim(pd.to_datetime(start_day), pd.to_datetime('2023-11-19'))
    plt.savefig(f'{output_dir}/{start_day}_{end_day}_{value1}{value2}.png', dpi=300, bbox_inches='tight')  # 파일명, 해상도 및 여백 설정

    plt.show()
#
# def draw_min_max(df, output_dir, start_date_str, end_date_str):
#     group_df = df
#     group_df['date'] = group_df['날짜'].dt.date
#     min_max = df.groupby('date').agg(max=('온도', 'max'),
#                                      min=('온도', 'min')).reset_index()
#
#
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.plot(min_max['date'], min_max['max'])
#     ax.plot(min_max['date'], min_max['min'])
#     plt.xticks(rotation=25)
#     plt.xlabel('날짜')
#     plt.ylabel(f'온도 (℃)')
#     plt.title(f'{start_date_str} ~ {end_date_str} | 최저 최고 온도')
#     plt.savefig(os.path.join(output_dir, f'{start_date_str}_{end_date_str}_최저최고온도.png'))

# def draw_min_max(df, output_dir, start_date_str, end_date_str):
#     group_df = df
#     group_df['date'] = group_df['시간'].dt.date
#     min_max_tem = df.groupby('date').agg(max=('온도', 'max'),
#                                      min=('온도', 'min')).reset_index()
#
#     min_max_hum = df.groupby('date').agg(max=('습도', 'max'),
#                                      min=('습도', 'min')).reset_index()
#
#     fig, ax1 = plt.subplots(figsize=(10, 8))
#     ax2 = ax1.twinx()
#
#     ax1.plot(min_max_tem['date'], min_max_tem['max'], color='green')
#     ax1.plot(min_max_tem['date'], min_max_tem['min'], color='green')
#     ax2.plot(min_max_hum['date'], min_max_hum['max'], color='red')
#     ax2.plot(min_max_hum['date'], min_max_hum['min'], color='red')
#     plt.xticks(rotation=25)
#     ax1.set_ylabel('온도', color='green')
#     ax2.set_ylabel('습도', color='red')
#
#     plt.xlabel('날짜')
#     plt.title(f'{start_date_str} ~ {end_date_str} | 최저 최고 온도 & 습도')
#
#
#     plt.show()
#
#     plt.savefig(os.path.join(output_dir, f'{start_date_str}_{end_date_str}_최저최고온도.png'))


def main():
    start_date_str = "20231113"
    end_date_str = "20231119"
    output_dir = f'./output/{start_date_str}_{end_date_str}'

    # figs(df, output_dir, '온도(°c)')
    # figs(df, output_dir, '습도(%)')
    figs(df, output_dir, 'GDD')
    # figs_2(df,output_dir, '온도(°c)', '습도(%)')

        # draw_min_max(df`, output_dir, start_date_str, end_date_str)

        # draw_min_max_hum`(df, output_dir, start_date_str, end_date_str)

if __name__=='__main__':
    main()





