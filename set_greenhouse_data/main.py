import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import numpy as np
import weather_df_cut

def cal_svp(temp):
    svp = 0.61078 * np.exp(np.array(temp) / (np.array(temp) + 233.3) * 17.2694)
    return svp

def cal_vpd(svp, hum):
    vpd = np.array(svp)*(1-np.array(hum)/100)
    return vpd

def cal_gdd(avg_temp):
    gdd = (np.array(avg_temp) -5 ).cumsum()
    return gdd
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

def draw_temp_graph(df, start_date, end_date):
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.lineplot(data=df, x='DAY', y='DAILY_TEMP_MEAN', label='DAILY_TEMP_MEAN')
    sns.lineplot(data=df, x='DAY', y='DAILY_TEMP_MAX', label='DAILY_TEMP_MAX')
    sns.lineplot(data=df, x='DAY', y='DAILY_TEMP_MIN', label='DAILY_TEMP_MIN')

    plt.legend(fontsize=15)
    ax.set_title(f'{start_date}_{end_date} | daily_temp graph.png', fontsize=20)
    ax.set_xlabel('Date'+'(YYYY-mm-dd)', fontsize=15)
    ax.set_ylabel('TEMP', fontsize=15)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    # ax.set_xticks(np.arange(0, len(df['DAY'])+1, 6))

    plt.savefig(f'output/graph/{start_date}_{end_date}_daily_temp.png')

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
    print(f'weather_df : {df}')

    return df
    #
    # draw_graph(graph_df, start_date, end_date, 'DLI')
    # draw_graph(graph_df, start_date, end_date, 'DIF')

def vpd_graph(df, start_date, end_date):
    x_label = sorted(set(df['Date']))
    vpd_df = df[['Date', 'VPD']]

    fig, ax = plt.subplots(figsize=(9, 9))
    sns.lineplot(data=vpd_df, x='Date', y='VPD')
    # plt.legend(fontsize=15)
    ax.set_title(f'{start_date}_{end_date} | VPD graph.png', fontsize=20)
    ax.set_xlabel('Date', fontsize=15)
    ax.set_ylabel('VPD', fontsize=15)
    ax.tick_params(axis='x', labelsize=15, rotation=15)
    ax.set_xticks(np.arange(0, len(x_label)+1, 6))
    ax.tick_params(axis='y', labelsize=15)

    plt.savefig(f'output/{start_date}_{end_date}_vpd.png')

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

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print('없음')
    else:
        print('있음')

    if not os.path.exists(file_name):
        print('파일이 없습니다')

    # 온실 데이터
    df = pd.read_csv(file_name)
    df['Date&Time'] = pd.to_datetime(df['Date&Time'])

    df.insert(1, 'Time', df['Date&Time'].astype(str).str.split(' ').str[1])
    df.insert(1, 'Date', df['Date&Time'].astype(str).str.split(' ').str[0])
    df = df[df['Date'].between(start_date, end_date)].reset_index()
    df = df.drop(['index'], axis=1)

    df['SVP'] = cal_svp(df['TEMP'])
    df['VPD'] = cal_vpd(df['SVP'], df['TEMP'])
    df[''] = ''
    daily_df = cal_avg_temp(df)

    df = pd.concat([df, daily_df], axis=1)
    df.to_csv(f'output/{start_date}_{end_date}_gh.csv')

    # draw_graph(df, start_date, end_date, 'DAILY_TEMP_MEAN')
    draw_temp_graph(df, start_date, end_date)

    # 여기까지 문제 x




    # draw_graph(df_2, start_date, end_date, 'DIF')
    # temp_graph(df_sorted, start_date, end_date)
    # vpd_graph(df_sorted, start_date, end_date)

    # 기상대 데이터
    # df_weather = pd.read_csv(f'output/{start_date}_{end_date}.csv')
    # weather_temp_graph(df_weather, start_date, end_date)


if __name__ == "__main__":
    # main('aM-31_data(24.02.13.).csv', '2023-09-13', '2023-10-26')
    main('aM-31_data(24.02.13.).csv', '2023-11-26', '2024-01-08')
