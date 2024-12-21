import aiohttp
from typing import Dict, Any
BASE_URL = "https://beta.chaingateway.io/api/v2/bsc"
@staticmethod
async def create_address(headers: Dict[str, str]) -> str:
        """
        Создает новый BSC-адрес через Chaingateway API.

        :param headers: Словарь с заголовками, включая токен авторизации.
        :return: Новый BSC-адрес.
        """
        url = f"{BASE_URL}/addresses/"
        payload = {"password": "123"}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status != 201:
                        raise Exception(f"Ошибка: {response.status}, {await response.text()}")
                    data = await response.json()
                    return data["data"]["bscaddress"]
            except Exception as e:
                raise Exception(f"Не удалось создать адрес: {e}")
@staticmethod
async def create_transaction(
    headers: Dict[str, str], 
    address_from: str, 
    address_to: str, 
    amount: float
) -> Any:
    """
    Создает транзакцию для перевода BNB.
    :param headers: Словарь с заголовками, включая токен авторизации.
    :param address_from: Адрес отправителя.
    :param address_to: Адрес получателя.
    :param amount: Сумма перевода в BNB.
    :return: Ответ API с данными о транзакции.
    """
    url = f"{BASE_URL}/transactions/"
    payload = {
        "from": address_from,
        "to": address_to,
        "amount": str(int(amount * 1e18)),  # Переводим BNB в Wei
        "gas": 21000,
        "gasprice": 1000000000,  # 1 Gwei
        "maxPriorityFeePerGas": 1000000000,
        "maxFeePerGas": 1000000000,
        "password": "123",
        "data": "0x",
        "nonce": "0"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Ошибка: {response.status}, {await response.text()}")
                return await response.json()
        except Exception as e:
            raise Exception(f"Не удалось создать транзакцию: {e}")
@staticmethod
async def get_balance(headers: Dict[str, str], address: str) -> float:
    """
    Получает баланс указанного BSC-адреса через Chaingateway API.
    :param headers: Словарь с заголовками, включая токен авторизации.
    :param address: BSC-адрес для проверки баланса.
    :return: Баланс в BNB.
    """
    url = f"{BASE_URL}/balances/{address}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Ошибка: {response.status}, {await response.text()}")
                data = await response.json()
                # Inspect the structure of the response to handle it correctly
                # Assuming the correct value is in 'data['data']['balance']', you may need to adjust this based on the API response.
                balance_data = data.get("data", {})
                # Add further validation depending on what the response contains
                if isinstance(balance_data, dict) and 'balance' in balance_data:

                    return float(balance_data['balance'])
                else:
                    raise Exception("Не удалось найти баланс в ответе API")
        except Exception as e:
            raise Exception(f"Не удалось получить баланс: {e}")