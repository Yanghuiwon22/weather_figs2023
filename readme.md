[//]: # (# set_greenhouse_data)

[//]: # ()
[//]: # (## 온실&기상데이터 시각화 )

[//]: # (|       항목        | 단위     | 수식 | 데이터 |)

[//]: # (|:---:|--------|----|-----|)

[//]: # (|       온도        | 섭씨&#40;°C&#41; |    | 온실  |)

[//]: # (|       VPD       |        |    | 온실  |)

[//]: # (|       GDD       |        |    | 온실  |)

[//]: # (|       DLI       |        |    | 기상대 |)

[//]: # (|       DIF       |        |    | 온실  |)

[//]: # ()
[//]: # (## 2023 케일 9월&#40;11월&#41;작기 그래프 &#40;예시&#41;)

[//]: # (|      항목      | 그래프                                                                                                                                  |)

[//]: # (|:------------:|----------------------------------------------------------------------------------------------------------------------------------------------|)

[//]: # (|    온도&#40;9월&#41;    | ![2023-09-13_2023-10-26_DAILY_TEMP]&#40;https://github.com/Yanghuiwon22/weather_figs_2023/assets/127187225/64e44f1d-27bd-4f0c-8d67-76e156bcb480&#41; |)

[//]: # (|   VPD &#40;9월&#41;   | ![2023-09-13_2023-10-26_VPD]&#40;https://github.com/Yanghuiwon22/weather_figs_2023/assets/127187225/08de38de-f6f3-4c3f-bff6-a97cb76dee14&#41;        |)

[//]: # (|   GDD &#40;9월&#41;   | ![2023-09-13_2023-10-26_GDD]&#40;https://github.com/Yanghuiwon22/weather_figs_2023/assets/127187225/35565fd4-b837-46b7-8535-7b1757c8392d&#41;        |)

[//]: # (|  DLI &#40;11월&#41;   | ![2023-11-27_2024-01-08_DLI]&#40;https://github.com/Yanghuiwon22/weather_figs_2023/assets/127187225/14b83ccd-10a8-40db-a936-b6b74dd6baea&#41;        |)

[//]: # (|   DIF &#40;9월&#41;   |  ![2023-09-13_2023-10-26_DIF_graph]&#40;https://github.com/Yanghuiwon22/weather_figs_2023/assets/127187225/2a7586a9-9a63-418c-8827-b3617e4f3180&#41; |)

[//]: # ()
[//]: # (## 참고자료)

[//]: # (- pega devlog &#40;데이터시각화 블로그&#41;)

[//]: # (  https://jehyunlee.github.io/2021/03/27/Python-DS-64-kr_pop_sn/)

[//]: # ()
[//]: # (## 기타)

[//]: # (온실데이터 : 전북대학교 원예학과 온실 <br>)

[//]: # (기상대데이터 : 전북대학교 학습도서관 옥상의 기상대)

## 2023 - 2024 케일 생육환경데이터 시각화
- 전북대학교 학습도서관 옥상 AWS 기상대와 전북대학교 원예학과 온실 환경데이터 사용했습니다.
- 학습도서관 옥상 AWS는 1분단위로 데이터가 수집되고, 온실은 60분위로 데이터가 수집됩니다.

### 사용법
- 기상대 데이터 다운로드
```python
import requests

year = 2023
month = 11

url = f"https://raw.githubusercontent.com/EthanSeok/JBNU_AWS/main/output/{year}_{month}.csv"
response = requests.get(url)

if response.status_code == 200:
    with open(f"{year}_{month}.csv", 'wb') as file:
        file.write(response.content)
    print(f"파일 {year}_{month}.csv을 다운로드했습니다.")
else:
    print(f"파일 다운로드에 실패했습니다. 상태 코드: {response.status_code}")
```
- 온실 데이터 다운로드
```python
import requests

url = f"https://github.com/Yanghuiwon22/weather_figs_2023/blob/main/set_greenhouse_data/greenhouse_data.csv"
response = requests.get(url)

if response.status_code == 200:
    with open(f"greenhouse_data.csv", 'wb') as file:
        file.write(response.content)
    print(f"파일 greenhouse_data.csv을 다운로드했습니다.")
else:
    print(f"파일 다운로드에 실패했습니다. 상태 코드: {response.status_code}")
```

