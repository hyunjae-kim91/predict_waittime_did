레스토랑 대기시간 예측

Docker image in Linux
1. sudo docker build -t predict:v1.x .
2. sudo docker images
3. sudo docker run -d -p 8000:8000 predict:v1.x

Local
1. pip install -r requirements.txt
2. bash run.sh
3. localhost:8000/docs 접속


### 프로젝트 구조
```
predict_waiting_did
├── app  # FastAPI 구동 폴더
|   ├── models 
|   |   ├── __init__.py
|   |   ├── model.py # Input, Output 정의
|   ├── predict
|   |   ├── __init__.py
|   |   ├── predict_router.py # 예측 및 로그 처리 모듈
├── models
|   ├── lambda_value.txt # y값 변환에 필요한 값 (필수)
|   ├── LGBM_V2.0.pkl # LightGBM 모델 피클 파일
|   ├── plantcode_mapping.yaml # 매장코드 라벨링 매핑 yaml 파일
├── nginx
|   ├── waiting.txt # y값 변환에 필요한 값 (필수)
├── logs # 로그 저장


├── .gitignore  # gitignore
├── requirements.txt  # python third party 패키지
├── .env  # 민감정보 환경변수로 관리
```