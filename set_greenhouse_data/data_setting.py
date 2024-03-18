import requests
import pandas as pd

start_date = '2023-11-27'
end_date = '2024-01-08'

date_list = [[2023, 11], [2023, 12], [2024, '01']]

def main():
    for month in date_list:
        url = f"https://raw.githubusercontent.com/EthanSeok/JBNU_AWS/main/output/{month[0]}_{month[1]}.csv"
        response = requests.get(url)

        if response.status_code == 200:
            with open(f"{month[0]}_{month[1]}.csv", 'wb') as file:
                file.write(response.content)
            print(f"파일 {month[0]}_{month[1]}.csv을 다운로드했습니다.")
        else:
            print(f"파일 다운로드에 실패했습니다. 상태 코드: {response.status_code}")

    total = pd.DataFrame()

    for month in date_list:
        temp = pd.read_csv(f'{month[0]}_{month[1]}.csv', encoding='utf-8')
        total = pd.concat([total, temp])

    total.to_csv(f'./output/{start_date}_{end_date}.csv', index=False)
    print(f'파일 ./output/{start_date}_{end_date}.csv을 다운로드했습니다')

if __name__=="__main__":
    main()

