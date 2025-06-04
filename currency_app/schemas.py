from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import List, Optional


class CurrencyRateRequest(BaseModel):
    base_currency: str = Field(default="USD", pattern="^[A-Z]{3}$")
    target_currency: str = Field(default="RUB", pattern="^[A-Z]{3}$")

    @classmethod
    def validate_currency_codes(cls, v):
        if len(v) != 3 or not v.isalpha():
            raise ValueError('Currency code must be 3 letters')
        return v.upper()


class CurrencyRateData(BaseModel):
    rate: Decimal = Field(..., gt=0, description="Курс валюты")
    source: str = Field(..., min_length=1, max_length=100)
    timestamp: datetime

    class Config:
        from_attributes = True


class CurrencyAPIResponse(BaseModel):
    current_rate: dict
    last_10_requests: List[dict]
    status: str = Field(default="success")

    class Config:
        from_attributes = True


class APIErrorResponse(BaseModel):
    status: str = Field(default="error")
    message: str
    error_code: Optional[str] = None
