from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class AddressRequest(BaseModel):
    """Схема для запроса информации о TRON-адресе."""

    address: str = Field(..., description="TRON-адрес для получения информации")


class TronAddressInfo(BaseModel):
    """Схема с информацией о TRON-адресе."""

    address: str = Field(..., description="TRON-адрес")
    bandwidth: str = Field(..., description="Bandwidth адреса")
    energy: str = Field(..., description="Energy адреса")
    balance: str = Field(..., description="Баланс в TRX")


class AddressQueryResponse(BaseModel):
    """Схема для записи о запросе адреса из БД."""

    id: uuid.UUID = Field(..., description="Уникальный идентификатор записи")
    address: str = Field(..., description="TRON-адрес")
    bandwidth: Optional[str] = Field(None, description="Bandwidth адреса")
    energy: Optional[str] = Field(None, description="Energy адреса")
    balance: Optional[str] = Field(None, description="Баланс в TRX")
    created_at: datetime = Field(..., description="Дата и время создания записи")

    class Config:
        from_attributes = True