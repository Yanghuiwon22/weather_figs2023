import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.ticker as ticker
from datetime import datetime, timedelta
from matplotlib.patches import Rectangle
import setting

plt.rcParams['font.family']='NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

dat_final = setting.dat_final
vpd_y_max = setting.vpd_y_max


def cal_svp(temp):
    svp = 0.61078 * np.exp(np.array(temp) / (np.array(temp) + 233.3) * 17.2694)
    return svp

def cal_dat_gh(day, start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    day = pd.to_datetime(day).dt.date
    dat = day - start
    return dat

def cal_vpd(svp, hum):
    vpd = np.array(svp)*(1-np.array(hum)/100)
    return vpd

def cal_gdd(df):
    df['GDD'] = (df['DAILY_TEMP_MEAN']-5).cumsum()
    return df

def cal_dli(df):
    print(df)
    grouped = df.groupby(df['Date'])
    x_label = []
    dli = []

    for date, group in grouped:
        x_label.append(date)

    daily_df = pd.DataFrame
    daily_df['DAY'] = x_label

    # df['DLI'] =
    # dli.append((group['PPF'].sum()) * 60 / 1000000)

    print(daily_df)

def cal_avg_temp(df):
    grouped = df.groupby(df['Date&Time'].dt.date)

    x_label = []
    temp_mean = []
    temp_max = []
    temp_min = []

    for date, group in grouped:
        x_label.append(date)
        temp_mean.append(group['TEMP'].mean())
        temp_max.append(group['TEMP'].max())
        temp_min.append(group['TEMP'].min())

    daily_df = pd.DataFrame()
    daily_df['DAY'] = x_label
    daily_df['DAILY_TEMP_MEAN'] = temp_mean
    daily_df['DAILY_TEMP_MAX'] = temp_max
    daily_df['DAILY_TEMP_MIN'] = temp_min

    return daily_df
def cal_y(df, col1, y):
    grouped = df.groupby(df['Date&Time'].dt.date)
    x_label = []
    y_list = []
    for date, group in grouped:
        x_label.append(date)
        y_list.append(group[col1].mean())

    daily_df = pd.DataFrame()
    daily_df['DAY'] = x_label
    daily_df[y] = y_list

    return daily_df

def draw_graph(df, start_date, end_date, y):
    fig, ax = plt.subplots(figsize=(11, 11))
    sns.lineplot(data=df, x='DAY', y=y, label=y)
    plt.legend(fontsize=15)
    ax.set_title(f'{start_date}_{end_date} | {y} graph.png', fontsize=20)
    ax.set_xlabel('Date'+'(YYYY-mm-dd)', fontsize=15)
    ax.set_ylabel(y, fontsize=15)
    ax.tick_params(axis='x', labelsize=15, rotation=15)
    ax.tick_params(axis='y', labelsize=15)
    # ax.set_xticks(np.arange(0, len(df['DAY'])+1, 6))

    plt.savefig(f'output/graph/{start_date}_{end_date}_{y}.png')

def draw_temp_graph(df, start_date, end_date, month):
    fig, ax = plt.subplots(figsize=(16, 9))
    color_mean = 'g'
    color_max = 'r'
    color_min = 'b'

    df_month = df[['DAY','DAT','DAILY_TEMP_MEAN','DAILY_TEMP_MAX', 'DAILY_TEMP_MIN']].dropna()
    df_month['DAT'] = df_month['DAT'].astype(int)
    df_month = df_month[df_month['DAT'].between(0, dat_final)]
    print(df_month)
    ax.plot(df_month['DAT'], df_month['DAILY_TEMP_MEAN'], c='g', lw=5, label='하루 평균 온도')
    ax.plot(df_month['DAT'], df_month['DAILY_TEMP_MAX'], c='r', lw=5, label='하루 중 최고 온도')
    ax.plot(df_month['DAT'], df_month['DAILY_TEMP_MIN'], c='b', lw=5, label='하루 중 최저 온도')

    # spines 정리
    for s in ["left", "right", "top"]:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_linewidth(3)

    ax.set_title(f"케일 {month}월작기 온도변화 추이", fontsize=24, fontweight="bold", pad=32)

    # 여름작기를 고려하여 y축 설정
    ax.set_ylim(-5, )
    ax.set_yticks([x*5 for x in range(-1, 10)])
    ax.set_yticklabels([f'{x*5}°C' for x in range(-1, 10)])

    # x축 눈금 + 제목 설정
    ax.xaxis.set_major_locator(ticker.MultipleLocator(8))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(4))
    plt.xlabel('정식 후 일자', fontsize=24, labelpad=10)

    # 그래프 옆 범례 표시
    mean_last = df_month['DAILY_TEMP_MEAN'][len(df_month)-1]
    max_last = df_month['DAILY_TEMP_MAX'][len(df_month)-1]
    min_last = df_month['DAILY_TEMP_MIN'][len(df_month)-1]

    font_xlabel = {"fontsize": 18, "ha": "left", "fontweight": "bold"}
    ax.text(1, (max_last+5)/(45-(-5)), "최고온도", transform=ax.transAxes, fontdict=font_xlabel, color=color_max)
    ax.text(1, (mean_last+5)/(45-(-5)), "평균온도", transform=ax.transAxes, fontdict=font_xlabel, color=color_mean)
    ax.text(1, (min_last+5)/(45-(-5)), "최저온도", transform=ax.transAxes, fontdict=font_xlabel, color=color_min)

    ax.grid(axis="y")
    ax.tick_params(axis='both', labelsize=20)

    ax.axvline(x=0, color='gray', linestyle='--')
    ax.axvline(x=42, color='gray', linestyle='--')
    ax.text(0, 1.03, f"     시작일\n{start_date}", transform=ax.transAxes, fontdict=font_xlabel, color='gray')
    ax.text(0.92, 1.03, f"     종료일\n{end_date}", transform=ax.transAxes, fontdict=font_xlabel, color='gray')

    plt.tight_layout()
    # plt.show()
    plt.savefig(f'output/graph/{start_date}_{end_date}_DAILY_TEMP.png')

def draw_vpd_graph(df, start_date, end_date, month):
    fig, ax = plt.subplots(figsize=(16, 9))
    color_vpd = 'k'

    df_month = df[['Date&Time', 'dat', 'VPD']]
    df_month.loc[:, 'dat'] = df_month['dat'].astype(int)

    df_month = df_month[df_month['dat'].between(0, dat_final)]
    ax.plot(df_month['Date&Time'], df_month['VPD'], c=color_vpd, lw=5, label='VPD')
    fig.legend(bbox_to_anchor=(0.86, 0.88),fontsize=24)

    # spines 정리
    for s in ["left", "right", "top"]:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_linewidth(3)

    # 그래프 제목
    ax.set_title(f"케일 {month}월작기 VPD", fontsize=24, fontweight="bold", pad=32)

    # # 여름작기를 고려하여 y축 설정
    ax.set_ylim(0, )
    ax.set_yticks([x for x in range(0,vpd_y_max+1)])
    ax.set_yticklabels([x for x in range(0,vpd_y_max+1)])

    # # x축 눈금 지정

    # # x축 눈금 + 제목 설정
    ax.xaxis.set_major_locator(ticker.MultipleLocator(8))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(4))
    plt.xlabel('정식 후 일자', fontsize=24, labelpad=10)
    #
    font_xlabel = {"fontsize": 18, "ha": "left", "fontweight": "bold"}
    ax.grid(axis="y")
    ax.tick_params(axis='both', labelsize=20)
    start_day = datetime.strptime(start_date, '%Y-%m-%d')
    end_day = datetime.strptime(end_date, '%Y-%m-%d')

    ax.axvline(x=start_day, color='gray', linestyle='--')
    ax.text(0, 1.03, f"     시작일\n{start_date}", transform=ax.transAxes, fontdict=font_xlabel, color='gray')
    #
    ax.fill_between([start_day, start_day+timedelta(dat_final)+timedelta(1)], 0.5, 1.2, color='g', alpha=0.15)
    ax.fill_between([start_day, start_day+timedelta(dat_final)+timedelta(1)], 0, 0.5, color='b', alpha=0.15)
    ax.fill_between([start_day, start_day+timedelta(dat_final)+timedelta(1)], 1.2, vpd_y_max, color='r', alpha=0.15)

    # 최적 범위 나타내기 ('ㄷ')
    range_x = 0.963
    plt.text(range_x, ((0.5+1.2)/2)/(vpd_y_max-0)-0.04, ' ', bbox=dict(facecolor='none', edgecolor='green', linewidth=5),
             transform=ax.transAxes, fontsize=65)
    for i in range(8):
        plt.text(range_x,((0.5+1.2)/2)/(vpd_y_max-0)-0.07+i*0.02, ' ', bbox=dict(facecolor='white', edgecolor='white', linewidth=5),
                 transform=ax.transAxes, fontsize=0.5)
    ax.text(range_x+0.035, ((0.5+1.2)/2)/(vpd_y_max-0), "적정 범위", transform=ax.transAxes, ha='left', va='center',
            fontsize=24, c='g', fontweight='bold')

    # x축 눈금 지정하기
    plt.xticks(ticks=[start_day, start_day+timedelta(8), start_day+timedelta(16), start_day+timedelta(24), start_day+timedelta(32), start_day+timedelta(40)],
               labels=['0', '8', '16', '24', '32', '40'])

    plt.tight_layout()
    # plt.show()
    plt.savefig(f'output/graph/{start_date}_{end_date}_VPD.png')

def draw_gdd_graph(df, start_date, end_date, month):
    # 데이터 정리
    df_month = df[['DAY', 'DAT', 'DAILY_TEMP_MEAN','GDD']].dropna()
    fontsize=24

    df_month['DAT'] = df_month['DAT'].astype(int)
    df_month = df_month[df_month['DAT'].between(0, dat_final) ]

    # 그래프 그리기 ( 기본 )
    fig, ax1 = plt.subplots(figsize=(16,9))
    ax1.plot(df_month['DAY'], df_month['GDD'], c='g', lw=5, label='GDD')
    plt.title(f'케일 {month}월작기 GDD', fontsize=fontsize, fontweight='bold')

    # -> bar plot
    ax2 = ax1.twinx()
    ax2.bar(df_month['DAY'], df_month['DAILY_TEMP_MEAN'], color='orange', alpha=0.3, label='하루 평균 온도')
    ax2.set_ylim(0, )
    ax2.set_yticks([x*5 for x in range(0,10)])
    ax2.set_yticklabels([f'{x*5}°C' for x in range(0,10)], fontsize=fontsize-3, color='orange', fontweight='bold')

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    fig.legend(handles1 + handles2, labels1 + labels2, (0.11,0.78),
               fontsize=fontsize - 3)

    # spines 정리
    for i in ['top', 'left', 'right']:
        ax1.spines[i].set_visible(False)
        ax2.spines[i].set_visible(False)
    ax1.spines['bottom'].set_linewidth(3)

    ax1.set_title(f"케일 {month}월작기 GDD", fontsize=24, fontweight="bold", pad=32)

    # 여름작기를 고려하여 y축 설정
    ax1.set_ylim(0, )
    ax1.set_yticks([x*100 for x in range(0, 10)])
    ax1.set_yticklabels([x*100 for x in range(0, 10)], color='g', fontweight='bold')

    # x축 눈금 + 제목 설정
    # ax1.xaxis.set_major_locator(ticker.MultipleLocator(8))
    # ax1.xaxis.set_minor_locator(ticker.MultipleLocator(4))
    plt.xlabel('날짜', fontsize=24, labelpad=10)

    # 그래프 옆 범례 표시
    font_xlabel = {"fontsize": 18, "ha": "left", "fontweight": "bold"}
    ax1.grid(axis="y")
    ax1.tick_params(axis='both', labelsize=20)

    start_day = datetime.strptime(start_date, '%Y-%m-%d')
    ax1.axvline(x=start_day, color='gray', linestyle='--')
    end_day = datetime.strptime(end_date, '%Y-%m-%d')
    # ax1.axvline(x=end_day + timedelta(1), color='gray', linestyle='--')
    ax1.text(0, 1.03, f"     시작일\n{start_date}", transform=ax1.transAxes, fontdict=font_xlabel, color='gray')
    # ax1.text(0.92, 1.03, f"     종료일\n{end_date}", transform=ax1.transAxes, fontdict=font_xlabel, color='gray')

    ax2.axhline(y=5, color='r', linestyle='-')
    ax2.text(0.875,0.13, '기준온도', color='r', transform=ax2.transAxes, fontsize=fontsize)

    plt.xticks(ticks=[start_day, start_day+timedelta(8), start_day+timedelta(16), start_day+timedelta(24), start_day+timedelta(32), start_day+timedelta(40)],
               labels=['0', '8', '16', '24', '32', '40'])


    plt.tight_layout()
    # plt.show()
    plt.savefig(f'output/graph/{start_date}_{end_date}_GDD.png')



def draw_dli_graph(df, start_date, end_date, month):
    print(df)
    # df_month = df[['Date', 'DAT','DLI']]
    fig, ax = plt.subplots()

    plt.show()
    plt.savefig(f'./output/graph/{start_date}_{end_date}_DLI.png')


def temp_graph(df, start_date, end_date):
    grouped = df.groupby(df['Date&Time'].dt.date)

    x_label = []
    temp_mean = []
    temp_max = []
    temp_min = []

    dif = []
    night_list = []
    day_list = []

    for date, group in grouped:
        group_temp = group['TEMP']
        temp_max.append(group_temp.max())
        temp_min.append(group_temp.min())
        temp_mean.append(group_temp.mean())
        x_label.append(date)

        night = group.loc[group['PPF'] == 0, 'TEMP']
        night_list.append(night)
        day = group.loc[group['PPF'] != 0, 'TEMP']
        day_list.append(day)

        dif.append(day-night)

    graph_df = pd.DataFrame()
    graph_df['Date'] = x_label
    graph_df['Temp_mean'] = temp_mean
    graph_df['Temp_max'] = temp_max
    graph_df['Temp_min'] = temp_min
    graph_df['GDD'] = (graph_df['Temp_mean']-5).cumsum()
    graph_df['DIF'] = dif

    print(graph_df)

    draw_graph(graph_df, start_date, end_date, 'DIF')

    return graph_df

def cal_daily_data(df, start_date, end_date):
    grouped = df.groupby(df['Date'])

    x_label = []
    dli = []

    dif = []
    night_list = []
    day_list= []

    for date, group in grouped:
        # dli
        dli.append((group['PPF'].sum())*60/1000000)

        # dif
        temp_mean_night = group.loc[group['PPF'] == 0, 'TEMP']
        temp_mean_day = group.loc[group['PPF'] != 0, 'TEMP']

        night = sum(temp_mean_night)/len(temp_mean_night)
        day = sum(temp_mean_day/len(temp_mean_day))

        dif.append(day-night)
        x_label.append(date)

        night_list.append(night)
        day_list.append(day)


    graph_df = pd.DataFrame()
    graph_df['DAY'] = x_label
    graph_df['DLI'] = dli
    graph_df['DIF'] = dif

    graph_df['day'] = day_list
    graph_df['night'] = night_list

    df = pd.concat([df, graph_df], axis=1)

    return df
    #
    # draw_graph(graph_df, start_date, end_date, 'DLI')
    # draw_graph(graph_df, start_date, end_date, 'DIF')

def gdd_graph(df, start_date, end_date):
    x_label = sorted(set(df['Date']))
    gdd_df = df[['Date', 'GDD']]

    fig, ax = plt.subplots(figsize=(9, 9))
    sns.lineplot(data=gdd_df, x='Date', y='GDD')
    # plt.legend(fontsize=15)
    ax.set_title(f'{start_date}_{end_date} | GDD graph.png', fontsize=20)
    ax.set_xlabel('Date', fontsize=15)
    ax.set_ylabel('GDD', fontsize=15)
    ax.tick_params(axis='x', labelsize=15, rotation=15)
    ax.set_xticks(np.arange(0, len(x_label)+1, 6))
    ax.tick_params(axis='y', labelsize=15)

    plt.savefig(f'output/{start_date}_{end_date}_gdd.png')

def main(file_name, start_date, end_date):
    output_dir = './output'
    greenhouse_data = './greenhouse_data.csv'
    weather_station_data = f'{output_dir}/{start_date}_{end_date}.csv'

    # 온실 데이터
    df_gh = pd.read_csv(greenhouse_data)
    df_gh['Date&Time'] = pd.to_datetime(df_gh['Date&Time'])

    df_gh.insert(1, 'Time', df_gh['Date&Time'].astype(str).str.split(' ').str[1])
    df_gh.insert(1, 'Date', df_gh['Date&Time'].astype(str).str.split(' ').str[0])
    df_gh = df_gh[df_gh['Date'].between(start_date, end_date)].reset_index()
    df_gh = df_gh.drop(['index'], axis=1)

    df_gh.insert(3, 'dat', cal_dat_gh(df_gh['Date'], start_date))
    df_gh['dat'] =df_gh['dat'].astype(str).str.split(' ').str[0]
    df_gh['SVP'] = cal_svp(df_gh['TEMP'])
    df_gh['VPD'] = cal_vpd(df_gh['SVP'], df_gh['TEMP'])
    df_gh[''] = ''
    daily_df = cal_avg_temp(df_gh)
    daily_df.insert(1, 'DAT', cal_dat_gh(daily_df['DAY'], start_date))
    daily_df['DAT'] = daily_df['DAT'].astype(str).str.split(' ').str[0]
    daily_df = cal_gdd(daily_df)

    df_gh = pd.concat([df_gh, daily_df], axis=1)
    df_gh.to_csv(f'output/{start_date}_{end_date}_gh.csv')

    # 그래프 그리기
    # draw_temp_graph(df_gh, start_date, end_date, datetime.strptime(start_date, '%Y-%m-%d').month)
    # print(f"""1. {datetime.strptime(start_date,'%Y-%m-%d').month}월 온도그래프 완""")
    # draw_vpd_graph(df_gh, start_date, end_date, datetime.strptime(start_date, '%Y-%m-%d').month)
    # print(f"""2. {datetime.strptime(start_date,'%Y-%m-%d').month}월 VPD 그래프 완""")
    # draw_gdd_graph(df_gh, start_date, end_date, datetime.strptime(start_date, '%Y-%m-%d').month)
    # print(f"""3. {datetime.strptime(start_date,'%Y-%m-%d').month}월 GDD 그래프 완""")

    # 기상대 데이터

    df_station = pd.read_csv(weather_station_data)
    df_station.insert(3, 'DAT', cal_dat_gh(df_station['Date'], start_date))
    df_station['DAT'] = df_station['DAT'].astype(str).str.split(' ').str[0]

    daily_df_2 = cal_dli(df_station)


    draw_dli_graph(df_station, start_date, end_date, datetime.strptime(start_date, '%Y-%m-%d').month)
    print(f'4. {datetime.strptime(start_date, "%Y-%m-%d").month}월 DLI 그래프 완')
    # draw_graph(df_2, start_date, end_date, 'DIF')
    # temp_graph(df_sorted, start_date, end_date)
    # vpd_graph(df_sorted, start_date, end_date)

    # 기상대 데이터
    # weather_temp_graph(df_weather, start_date, end_date)


if __name__ == "__main__":
    # main('greenhouse_data.csv', '2023-09-13', '2023-10-26')
    main('greenhouse_data.csv', '2023-11-27', '2024-01-08')
