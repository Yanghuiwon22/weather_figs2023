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

    fig, ax = plt.subplots(figsize=(9, 9))
    sns.lineplot(data=graph_df, x='Date', y='Temp_mean', label='Temp_mean')
    sns.lineplot(data=graph_df, x='Date', y='Temp_max', label='Temp_max')
    sns.lineplot(data=graph_df, x='Date', y='Temp_min', label='Temp_min')
    plt.legend(fontsize=15)
    ax.set_title(f'{start_date}_{end_date} | temp. graph.png', fontsize=20)
    ax.set_xlabel('Date', fontsize=15)
    ax.set_ylabel('Temp', fontsize=15)
    ax.tick_params(axis='x', labelsize=15, rotation=15)
    ax.tick_params(axis='y', labelsize=15)

    plt.savefig(f'output/{start_date}_{end_date}_temp.png')

def vpd_graph(df, start_date, end_date):
    grouped = df.groupby(df['Date&Time'].dt.date)

    x_label = []
    vpd = []


    for date, group in grouped:
        group_temp = group['TEMP']
        temp_max.append(group_temp.max())
        temp_min.append(group_temp.min())

        temp_mean.append(group_temp.mean())
        x_label.append(date)

    graph_df = pd.DataFrame()
    graph_df['Date'] = x_label
    graph_df['Temp_mean'] = temp_mean


    fig, ax = plt.subplots(figsize=(9, 9))
    sns.lineplot(data=graph_df, x='Date', y='Temp_mean', label='Temp_mean')
    sns.lineplot(data=graph_df, x='Date', y='Temp_max', label='Temp_max')
    sns.lineplot(data=graph_df, x='Date', y='Temp_min', label='Temp_min')
    plt.legend(fontsize=15)
    ax.set_title(f'{start_date}_{end_date} | temp. graph.png', fontsize=20)
    ax.set_xlabel('Date', fontsize=15)
    ax.set_ylabel('Temp', fontsize=15)
    ax.tick_params(axis='x', labelsize=15, rotation=15)
    ax.tick_params(axis='y', labelsize=15)

    plt.savefig(f'output/{start_date}_{end_date}_temp.png')




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
    # df_sorted['VPD'] = cal_vpd(df_sorted['SVP'].astype(float), df['HUMI'].astype(float))

    print(df_sorted)

    # temp_graph(df_sorted, start_date, end_date)



if __name__ == "__main__":
    main('aM-31_data(24.02.13.).csv', '2023-11-26', '2024-01-08')
