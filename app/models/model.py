from pydantic import BaseModel, Field, validator
from datetime import datetime

class CustomValidationException(Exception):
    def __init__(self, message: str):
        self.message = message

class InputModel(BaseModel):
    """input parameter"""
    shopList: list = Field()
    daytype: int = Field(default=2)
    regidatetime: str = Field(default='2023-12-01 12:00:00')

    @validator("regidatetime")
    def validate_regitime_format(cls, value):
        try:
            # 날짜 및 시간 형식이 맞는지 확인
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return value
        except ValueError:
            raise CustomValidationException("올바른 날짜 및 시간 형식이 아닙니다. 'yyyy-mm-dd hh:mm:ss' 형식을 사용하세요.")
    
    @validator("daytype")
    def validate_daytype(cls, value):
        if value not in (1, 2, 3):
            raise CustomValidationException("날짜 형식은 1, 2, 3 중 하나입니다.")
        return value

class OutputModel(BaseModel):
    resultFlag : bool
    resultData: list = Field()
    errCode: str
    errMessage: str