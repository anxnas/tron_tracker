from sqlalchemy import Column, String

from app.models.base import BaseModel


class AddressQuery(BaseModel):
    """
    Модель для хранения запросов к TRON-адресам.

    Хранит информацию о запрошенных TRON-адресах и их ресурсах, включая
    bandwidth, energy и баланс в TRX. Каждая запись представляет собой
    отдельный запрос к API.
    """

    address = Column(String, nullable=False, index=True, comment="TRON-адрес, для которого был выполнен запрос")
    bandwidth = Column(String, nullable=True, comment="Bandwidth адреса (в единицах TRON) на момент запроса")
    energy = Column(String, nullable=True, comment="Energy адреса (в единицах TRON) на момент запроса")
    balance = Column(String, nullable=True, comment="Баланс адреса в TRX на момент запроса")