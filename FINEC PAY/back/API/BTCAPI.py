import aiohttp
from typing import Dict, Any, Optional

BASE_URL = "https://beta.chaingateway.io/api/v2/bitcoin"

class BitcoinAPI:
    @staticmethod
    async def create_wallet(headers: Dict[str, str], password: str = "strongpassword") -> str:
        """
        Создаёт новый Bitcoin-кошелёк через Chaingateway API.

        :param headers: Словарь с заголовками, включая токен авторизации.
        :param password: Пароль для кошелька.
        :return: Имя созданного кошелька (например: "01HP6FVARVTQES6WW8QHC5WHPT").
        """
        url = f"{BASE_URL}/wallets"
        payload = {
            "password": password
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status != 201:
                        raise Exception(f"Ошибка при создании кошелька: {response.status}, {await response.text()}")
                    data = await response.json()
                    # Пример ответа:
                    # {
                    #   "status": 201,
                    #   "ok": true,
                    #   "message": "Address created",
                    #   "data": {
                    #     "bitcoinwallet": "01HP6FVARVTQES6WW8QHC5WHPT"
                    #   }
                    # }
                    wallet_data = data.get("data", {})
                    if "bitcoinwallet" in wallet_data:
                        return wallet_data["bitcoinwallet"]
                    else:
                        raise Exception("Не удалось найти имя кошелька в ответе API")
            except Exception as e:
                raise Exception(f"Не удалось создать кошелёк: {e}")

    @staticmethod
    async def get_balance(headers: Dict[str, str], wallet_or_address: str) -> Any:
        """
        Получает информацию о кошельке или адресе.
        
        :param headers: Словарь с заголовками, включая токен авторизации.
        :param wallet_or_address: Либо имя кошелька (bitcoinwallet), либо непосредственно BTC-адрес.
        :return: Ответ API с информацией о кошельке или адресе.
        """
        url = f"{BASE_URL}/wallets/{wallet_or_address}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"Ошибка при получении данных: {response.status}, {await response.text()}")
                    data = await response.json()
              
                    return data["data"]['balance']
            except Exception as e:
                raise Exception(f"Не удалось получить данные о кошельке или адресе: {e}")

    @staticmethod
    async def create_address_in_wallet(headers: Dict[str, str], walletname: str) -> str:
        """
        Создаёт новый адрес внутри указанного биткоин-кошелька.
        
        :param headers: Словарь с заголовками, включая токен авторизации.
        :param walletname: Имя кошелька, полученное при создании.
        :return: Новый BTC-адрес.
        """
        url = f"{BASE_URL}/wallets/{walletname}/addresses"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers) as response:
                    if response.status != 201:
                        raise Exception(f"Ошибка при создании адреса: {response.status}, {await response.text()}")
                    data = await response.json()
                    # Пример ответа:
                    # {
                    #   "status": 201,
                    #   "ok": true,
                    #   "message": "Address created",
                    #   "data": {
                    #     "address": "bc1qzq8m9ukvvgvj7kmlejnfr2q4ndmk2e4ndtr9rn"
                    #   }
                    # }
                    address_data = data.get("data", {})
                    if "address" in address_data:
                        return address_data["address"]
                    else:
                        raise Exception("Не удалось найти адрес в ответе API")
            except Exception as e:
                raise Exception(f"Не удалось создать адрес в кошельке: {e}")

    @staticmethod
    async def create_transaction(
        headers: Dict[str, str],
        to_address: str,
        amount_btc: float,
        walletname: str,
        password: str,
        subtractfee: bool = True,
        speed: str = "high"
    ) -> Any:
        """
        Создаёт транзакцию по переводу BTC.
        
        :param headers: Словарь с заголовками, включая токен авторизации.
        :param to_address: Адрес получателя (например: "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq").
        :param amount_btc: Сумма перевода в BTC (например: 0.0001).
        :param walletname: Имя кошелька, из которого отправляются средства.
        :param password: Пароль, установленный при создании кошелька.
        :param subtractfee: Если True, комиссия будет вычтена из отправляемой суммы.
        :param speed: Скорость транзакции (например: "high").
        :return: Ответ API с данными о транзакции, включая txid.
        """
        url = f"{BASE_URL}/transactions"
        payload = {
            "to": to_address,
            "amount": amount_btc,
            "walletname": walletname,
            "password": password,
            "subtractfee": subtractfee,
            "speed": speed
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status != 201:
                        raise Exception(f"Ошибка при создании транзакции: {response.status}, {await response.text()}")
                    data = await response.json()
                    # Пример ответа:
                    # {
                    #   "status": 201,
                    #   "ok": true,
                    #   "message": "Succesfully created transaction",
                    #   "data": {
                    #     "txid": "9aede7eee01b79aab1cd5a8990f31069756bdf9c969c67b1fd90428ece11919f"
                    #   }
                    # }
                    return data
            except Exception as e:
                raise Exception(f"Не удалось создать транзакцию: {e}")
