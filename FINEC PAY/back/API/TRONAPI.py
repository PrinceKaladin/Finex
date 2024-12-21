import aiohttp
from typing import Dict, Any

BASE_URL = "https://beta.chaingateway.io/api/v2/tron"

class TronAPI:
    @staticmethod
    async def create_address(headers: Dict[str, str]) -> str:
        """
        Создает новый Tron-адрес через Chaingateway API.

        :param headers: Словарь с заголовками, включая токен авторизации.
        :return: Новый Tron-адрес.
        """
        url = f"{BASE_URL}/addresses"
        # По документации нужно указать пароль (хотя в примере не показан).
        # Также можно включить activated для автоматической активации.
        payload = {
            "activated": False,
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status != 201:
                        raise Exception(f"Ошибка: {response.status}, {await response.text()}")
                    data = await response.json()
                    # Возвращаем Tron-адрес из ответа
                    # data["data"] – это список, первый элемент содержит данные о созданном адресе
                    return [data["data"]["address"],data["data"]["privateKey"]]
            except Exception as e:
                raise Exception(f"Не удалось создать адрес: {e}")

    @staticmethod
    async def create_transaction(
        headers: Dict[str, str], 
        private_key: str, 
        address_from: str, 
        address_to: str, 
        amount: float
    ) -> Any:
        """
        Создает транзакцию на перевод TRX.
        
        :param headers: Словарь с заголовками, включая токен авторизации.
        :param private_key: Приватный ключ адреса отправителя.
        :param address_from: Адрес отправителя.
        :param address_to: Адрес получателя.
        :param amount: Сумма перевода в TRX.
        :return: Ответ API с данными о транзакции.
        """
        url = f"{BASE_URL}/transactions"
        payload = {
            "amount": amount,
            "privatekey": private_key,
            "to": address_to,
            "from": address_from
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    # Если транзакция успешно создана, ожидается статус 201
                    if response.status != 201:
                        raise Exception(f"Ошибка: {response.status}, {await response.text()}")
                    return await response.json()
            except Exception as e:
                raise Exception(f"Не удалось создать транзакцию: {e}")

    @staticmethod
    async def get_balance(headers: Dict[str, str], address: str) -> float:
        """
        Получает баланс указанного Tron-адреса через Chaingateway API.
        
        :param headers: Словарь с заголовками, включая токен авторизации.
        :param address: Tron-адрес для проверки баланса.
        :return: Баланс в TRX.
        """
        url = f"{BASE_URL}/balances/{address}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"Ошибка: {response.status}, {await response.text()}")
                    data = await response.json()
                    # По примеру из документации balance находится в data["data"]["balance"]
                    balance_data = data.get("data", {})
                    if isinstance(balance_data, dict) and 'balance' in balance_data:
                        return float(balance_data['balance'])
                    else:
                        raise Exception("Не удалось найти баланс в ответе API")
            except Exception as e:
                raise Exception(f"Не удалось получить баланс: {e}")
