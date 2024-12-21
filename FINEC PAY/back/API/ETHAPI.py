import aiohttp
from typing import Dict, Any

BASE_URL = "https://beta.chaingateway.io/api/v2/ethereum"

class EthereumAPI:
    @staticmethod
    async def create_address(headers: Dict[str, str], password: str = "strongpassword") -> str:
        """
        Создает новый Ethereum-адрес через Chaingateway API.

        :param headers: Словарь с заголовками, включая токен авторизации.
        :param password: Пароль, необходимый для кошелька.
        :return: Новый Ethereum-адрес (строка).
        """
        url = f"{BASE_URL}/addresses"
        payload = {
            "password": password
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    # Ожидаемый статус при успешном создании: 201
                    if response.status != 201:
                        raise Exception(f"Ошибка при создании адреса: {response.status}, {await response.text()}")
                    data = await response.json()
                    # Пример ответа:
                    # {
                    #   "status": 201,
                    #   "ok": true,
                    #   "message": "Address created",
                    #   "data": {
                    #     "adderess": "0x7d3bC832A0860fD882FF4C2359e10268f4E5CCf8"
                    #   }
                    # }
                    address_data = data.get("data", {})
   
                    if "ethereumaddress" in address_data:
                        return address_data["ethereumaddress"]
                    else:
                        raise Exception("Не удалось найти адрес в ответе API")
            except Exception as e:
                raise Exception(f"Не удалось создать адрес: {e}")

    @staticmethod
    async def get_balance(headers: Dict[str, str], address: str) -> float:
        """
        Получает баланс указанного Ethereum-адреса через Chaingateway API.
        
        :param headers: Словарь с заголовками, включая токен авторизации.
        :param address: Ethereum-адрес для проверки баланса.
        :return: Баланс в ETH.
        """
        url = f"{BASE_URL}/balances/{address}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"Ошибка при получении баланса: {response.status}, {await response.text()}")
                    data = await response.json()
                    # Пример ответа:
                    # {
                    #   "status": 200,
                    #   "ok": true,
                    #   "message": "Balance fetched",
                    #   "data": "0.000000000000000000"
                    # }
                    balance_str = data['data']['balance']
                    return float(balance_str)
            except Exception as e:
                raise Exception(f"Не удалось получить баланс: {e}")

    @staticmethod
    async def create_transaction(
        headers: Dict[str, str],
        private_key: str,
        address_from: str,
        address_to: str,
        amount_eth: float,
        password: str = "strongpassword",
        gas: int = 21000,
        gasprice: int = 1000000000,
        maxPriorityFeePerGas: int = 1000000000,
        maxFeePerGas: int = 1000000000,
        data_hex: str = "0x",
        nonce: str = "0"
    ) -> Any:
        """
        Создает транзакцию для перевода ETH.
        
        Предполагается, что Chaingateway API для Ethereum работает подобно BSC или Tron.
        Проверяйте актуальную документацию.

        :param headers: Словарь с заголовками, включая токен авторизации.
        :param private_key: Приватный ключ адреса отправителя (при необходимости).
        :param address_from: Адрес отправителя (0x...).
        :param address_to: Адрес получателя (0x...).
        :param amount_eth: Сумма перевода в ETH.
        :param password: Пароль для кошелька, если он требуется.
        :param gas: Лимит газа для транзакции.
        :param gasprice: Цена газа (Wei).
        :param maxPriorityFeePerGas: maxPriorityFeePerGas (для EIP-1559 транзакций).
        :param maxFeePerGas: maxFeePerGas (для EIP-1559 транзакций).
        :param data_hex: Данные для транзакции (по умолчанию 0x).
        :param nonce: Номер nonce (по умолчанию "0", или можно не указывать).
        :return: Ответ API с информацией о транзакции.
        """
        url = f"{BASE_URL}/transactions"
        # Переведём amount_eth в Wei: 1 ETH = 10^18 Wei
        amount_wei = str(int(amount_eth * (10 ** 18)))

        payload = {
            "from": address_from,
            "to": address_to,
            "amount": amount_wei,
            "gas": gas,
            "gasprice": gasprice,
            "maxPriorityFeePerGas": maxPriorityFeePerGas,
            "maxFeePerGas": maxFeePerGas,
            "password": password,
            "data": data_hex,
            "nonce": nonce,
            # Если требуется, может быть нужна форма {"privatekey": private_key}
            # в зависимости от того, как Chaingateway ожидает подписания транзакций.
            # Если нужен приватный ключ:

        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    # Уточните ожидаемый статус-код в документации.
                    # Предположим, что при успехе вернётся 201.
                    if response.status != 201:
                        raise Exception(f"Ошибка при создании транзакции: {response.status}, {await response.text()}")
                    return await response.json()
            except Exception as e:
                raise Exception(f"Не удалось создать транзакцию: {e}")

    @staticmethod
    async def get_transaction_info(headers: Dict[str, str], tx_hash: str) -> Any:
        """
        Получает информацию о транзакции по её хэшу.
        
        :param headers: Словарь с заголовками, включая токен авторизации.
        :param tx_hash: Хэш транзакции (0x...).
        :return: Ответ API с информацией о транзакции.
        """
        url = f"{BASE_URL}/transactions/{tx_hash}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"Ошибка при получении данных транзакции: {response.status}, {await response.text()}")
                    data = await response.json()
                    return data
            except Exception as e:
                raise Exception(f"Не удалось получить данные о транзакции: {e}")
