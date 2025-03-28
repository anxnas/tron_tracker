from tronpy import Tron
from tronpy.exceptions import (
    ApiError,
    AddressNotFound,
    NotFound,
    UnknownError,
    ValidationError,
    BadAddress
)
from typing import Dict, Any

from app.config import settings
from app.utils import log
from app.exceptions import TronAPIException, TronAddressNotFoundException, TronNetworkException


class TronService:
    """Сервис для работы с TRON API."""

    def __init__(self):
        """Инициализация клиента TRON API."""
        if settings.TRON_API_KEY:
            self.client = Tron(network='mainnet', api_key=settings.TRON_API_KEY)
        else:
            self.client = Tron(network='mainnet')

    async def get_address_info(self, address: str) -> Dict[str, Any]:
        """
        Получение информации о TRON-адресе.

        Args:
            address: TRON-адрес

        Returns:
            Dict: Информация о адресе (bandwidth, energy, баланс)

        Raises:
            TronAddressNotFoundException: Если адрес не найден
            TronNetworkException: При ошибке сети
            TronAPIException: При других ошибках TRON API
        """
        try:
            log.info(f"Запрос информации для адреса {address}")

            # Проверка формата адреса
            try:
                # Валидация формата адреса может вызвать BadAddress
                if not address.startswith('T') or len(address) != 34:
                    raise BadAddress("Некорректный формат TRON-адреса")
            except BadAddress as e:
                log.error(f"Некорректный формат адреса: {str(e)}")
                raise TronAddressNotFoundException(f"Некорректный формат TRON-адреса: {str(e)}")

            # Получаем аккаунт
            try:
                account = self.client.get_account(address)
            except AddressNotFound as e:
                log.error(f"Адрес {address} не найден: {str(e)}")
                raise TronAddressNotFoundException(f"Адрес {address} не найден в сети TRON")
            except NotFound as e:
                log.error(f"Ресурс не найден: {str(e)}")
                raise TronAddressNotFoundException(f"Ресурс не найден: {str(e)}")

            # Получаем bandwidth и energy
            try:
                account_resource = self.client.get_account_resource(address)
            except ApiError as e:
                log.error(f"Ошибка API при получении ресурсов аккаунта: {str(e)}")
                raise TronNetworkException(f"Ошибка API при получении ресурсов аккаунта: {str(e)}")
            except Exception as e:
                log.error(f"Ошибка при получении ресурсов аккаунта: {str(e)}")
                raise TronNetworkException(f"Ошибка при получении ресурсов аккаунта: {str(e)}")

            # Получаем баланс в TRX
            try:
                balance = self.client.get_account_balance(address)
            except ApiError as e:
                log.error(f"Ошибка API при получении баланса: {str(e)}")
                raise TronNetworkException(f"Ошибка API при получении баланса: {str(e)}")
            except Exception as e:
                log.error(f"Ошибка при получении баланса: {str(e)}")
                raise TronNetworkException(f"Ошибка при получении баланса: {str(e)}")

            # Формируем результат
            bandwidth = str(account_resource.get("freeNetLimit", 0)) if account_resource else "0"
            energy = str(account_resource.get("EnergyLimit", 0)) if account_resource else "0"

            return {
                "address": address,
                "bandwidth": bandwidth,
                "energy": energy,
                "balance": str(balance)
            }
        except (TronAddressNotFoundException, TronNetworkException):
            # Пробрасываем уже созданные исключения
            raise
        except ValidationError as e:
            log.error(f"Ошибка валидации данных TRON API: {str(e)}")
            raise TronAPIException(f"Ошибка валидации данных TRON API: {str(e)}")
        except ApiError as e:
            log.error(f"Ошибка TRON API: {str(e)}")
            raise TronAPIException(f"Ошибка при взаимодействии с TRON API: {str(e)}")
        except UnknownError as e:
            log.error(f"Неизвестная ошибка TRON API: {str(e)}")
            raise TronAPIException(f"Неизвестная ошибка при взаимодействии с TRON API: {str(e)}")
        except Exception as e:
            log.error(f"Неожиданная ошибка при получении данных из TRON API: {str(e)}")
            raise TronAPIException(f"Неожиданная ошибка при взаимодействии с TRON API: {str(e)}")