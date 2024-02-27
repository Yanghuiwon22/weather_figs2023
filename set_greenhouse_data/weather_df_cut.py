import pandas as pd

start_date = '2023-09-13'
end_date = '2023-10-26'

def get_df_weather():
    raw_df_weather = pd.read_csv('output/2023-09-13 - 2023-11-26.csv')
    df_weather = raw_df_weather[raw_df_weather['날짜'].between(start_date,end_date)].reset_index()

    return df_weather

def main():
    result = get_df_weather()
    return result
if __name__=="__main__":
    
    main()



