import yaml

from typing import Tuple
import pandas as pd
from datetime import datetime
from scipy.special import inv_boxcox

# week_no 1년(52주) 중 해당 날짜가 속한 주
# week_int 월별 주차정보 (1~5)
# dayno 1 : 일 / 2 : 월 / 3 : 화 / 4 : 수 / 5 : 목 / 6 : 금 / 7 : 토
# regihour : 시간
# regiminute : 초 제거하고 '분'로 변환 Ex. 10:06:38 -> 10:06:00 -> 10*60 + 6 = 606
# regisecond : 시간을 모두 '초'로 변환 Ex.10:06:38 -> 10*3600+60*6+38=36398

# plantcode 매핑 파일 읽기
with open('models/plantcode_mapping.yaml', 'r') as file:
    plantcode_mapping = yaml.safe_load(file)

# Box-cox 변환
with open('models/lambda_value.txt', 'r') as f:
    lambda_value = float(f.read())

# 고객 리스트
customer_list = [2, 4, 6]

def transform_plantcode(plantcode: str) -> int:
    return plantcode_mapping.get(plantcode, -1)

def transform_time(date_str: str) -> Tuple[int, int, int]:
    hour, minute, second = map(int, date_str.split(':'))
    regihour = hour
    regiminute = hour * 60 + minute
    regisecond = hour * 3600 + minute * 60 + second
    return regihour, regiminute, regisecond

def extract_week(date_str: str) -> int:
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    iso_week_number = date_obj.isocalendar()[1]
    return iso_week_number

def extract_dayno(date_str: str) -> int:
      return (datetime.strptime(date_str, '%Y-%m-%d').weekday() + 2) % 7 or 7

def transform_dataframe(request_body: dict) -> pd.DataFrame:

    date_str, time_str = request_body['regidatetime'].split(' ')
    regihour, regiminute, regisecond = transform_time(time_str)

    df = pd.DataFrame([{
            'plantcode_L' : transform_plantcode(row['plantcode']),
            'week_no' : extract_week(date_str),
            'waitingno' : row['waitingno'],
            'dayno' : extract_dayno(date_str),
            'daytype' : request_body['daytype'],
            'regihour' : regihour,
            'regiminute' : regiminute,
            'regisecond' : regisecond,
            'teamahead' : row['teamahead'],
            'customercnt' : i,
            'customergroupcnt' : i,
    } for row in request_body['shopList'] for i in customer_list])
    return df

def transform_pred(predict: list) -> list:
    # 1. 분 환산 (올림)
    prediction = [int(inv_boxcox(pred, lambda_value)/60)+1 for pred in predict]
    return prediction

def get_response_form(request_body: dict, prediction: list) -> pd.DataFrame:
    list_length = len(customer_list)
    prediction_split = [prediction[i*list_length:(i+1)*list_length] for i in range(int(len(prediction)/list_length))]
    result = pd.DataFrame([{
        'plantcode' : row['plantcode'],
        'waittime2' : waittime2,
        'waittime4' : waittime4,
        'waittime6' : waittime6,
    } for row, [waittime2, waittime4, waittime6] in zip(request_body['shopList'], prediction_split)])
    result = result.to_dict(orient='records')
    return result