import pandas as pd

def first():
    file_name = '경상북도농업기술원0104'
    df = pd.read_csv(f'./task/22작기/경상북도농업기술원/{file_name}_정리된_데이터.csv')

    print(df.columns)


    df.insert(1, ' ', df['ts_round'].str.split(' ').str[0])
    df.insert(2, '', df['ts_round'].str.split(' ').str[1].str[:-6])

    df_2 = df.reindex(['Timestamp', '',' ','배지EC 1(dS/m)',
                       '배지수분함량 1(%)', '배지온도 1(°c)', '내부순간광량 1(W/m2)',
                       '내부누적광량(J/cm2)', '배지무게 1(kg)', '배지EC 1(dS/m)','내부상대습도 1(%)',
                       '내부온도 1(°c)', '내부CO2농도 1(ppm)', '순간 증산량(kg/min)', '순간 증산량 보정1',
                       '순간 증산량 보정2', '순간 증산량 보정3', '날짜', '평균 온도', '습도', 'SVP', 'VPD',
                       '일 평균 광량(W/m2)', '일 누적 광량 (MJ/m2)', '일평균 분당 증산량(kg/min)',
                       '일 누적 증산량 (kg)',], axis=1)



    df_2.to_csv(f'./output/{file_name}_정리된_데이터.csv', encoding='utf-8-sig', index=False)
def second():
    df_2 = pd.read_csv('./output/korea_0101.csv')
    df_2['시간 변경'] = pd.to_datetime(df_2['시간'])

if __name__=="__main__":
    first()


