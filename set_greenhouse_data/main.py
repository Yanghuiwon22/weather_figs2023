import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import numpy as np
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
    try:
        print('try')
        grouped = df.groupby(df['Date&Time'].dt.date)

        avg_temp = []
        for date, group in grouped:
            group_temp = group['TEMP']
            temp_mean = group_temp.mean()

            avg_temp.extend([temp_mean for i in range(len(group))])

        df['avg_temp'] = avg_temp
        print(df)
    except ValueError:
        print('except')
        pass

    return df

def draw_graph(df, start_date, end_date, y):
    print(f'df = {df}')
    fig, ax = plt.subplots(figsize=(9, 9))
    sns.lineplot(data=df, x='Date', y=y, label='Temp_mean')
    plt.legend(fontsize=15)
    ax.set_title(f'{start_date}_{end_date} | {y} graph.png', fontsize=20)
    ax.set_xlabel('Date', fontsize=15)
    ax.set_ylabel(y, fontsize=15)
    ax.tick_params(axis='x', labelsize=15, rotation=15)
    ax.tick_params(axis='y', labelsize=15)
    plt.ylim(0,850)

    plt.savefig(f'output/{start_date}_{end_date}_{y}.png')


def temp_graph(df, start_date, end_date):
    grouped = df.groupby(df['Date&Time'].dt.date)

    x_label = []
    temp_mean = []
    temp_max = []
    temp_min = []

    for date, group in grouped:
        group_temp = group['TEMP']
        temp_max.append(group_temp.max())
        temp_min.append(group_temp.min())
        temp_mean.append(group_temp.mean())
        x_label.append(date)

    graph_df = pd.DataFrame()
    graph_df['Date'] = x_label
    graph_df['Temp_mean'] = temp_mean
    graph_df['Temp_max'] = temp_max
    graph_df['Temp_min'] = temp_min
    graph_df['GDD'] = (graph_df['Temp_mean']-5).cumsum()

    draw_graph(graph_df, start_date, end_date, 'GDD')

    return graph_df



def vpd_graph(df, start_date, end_date):
    x_label = sorted(set(df['Date']))
    print(x_label)
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

    # 9월 작기
    # start_date = '2023-09-13'
    # end_date = '2023-10-27'

    # 11월 작기
    # start_date = '2023-11-26'
    # end_date = '2024-01-08'

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print('없음')
    else:
        print('있음')

    if not os.path.exists(file_name):
        print('파일이 없습니다. 파일이 있을경우 이름을 확인해주세요! (aM-31_data)')

    df = pd.read_csv(file_name)
    df['Date&Time'] = pd.to_datetime(df['Date&Time'])

    df.insert(1, 'Time', df['Date&Time'].astype(str).str.split(' ').str[1])
    df.insert(1, 'Date', df['Date&Time'].astype(str).str.split(' ').str[0])

    df_sorted = df[df['Date'].between(start_date, end_date)].reset_index()
    df_sorted = df_sorted.drop(['index'], axis=1)

    df_sorted['SVP'] = cal_svp(df_sorted['TEMP'])
    df_sorted['VPD'] = cal_vpd(df_sorted['SVP'], df_sorted['TEMP'])
    df_sorted = cal_avg_temp(df_sorted)
    df_sorted['GDD'] = cal_gdd(df_sorted['avg_temp'])

    df_2 = cal_avg_temp(df_sorted)

    draw_graph(df_2, start_date, end_date, 'GDD')
    temp_graph(df_sorted, start_date, end_date)
    vpd_graph(df_sorted, start_date, end_date)



if __name__ == "__main__":
    main('aM-31_data(24.02.13.).csv', '2023-09-13', '2023-10-27')
    main('aM-31_data(24.02.13.).csv', '2023-11-26', '2024-01-08')
