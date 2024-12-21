import aiohttp
from typing import Dict, Any

class USDTAPI:
    # Данные для каждой сети
    NETWORK_CONFIG = {
        "ethereum": {
            "base_url": "https://beta.chaingateway.io/api/v2/ethereum",
            "usdt_contract": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "balance_endpoint": "balances/{address}/erc20/{contract}",
            "address_endpoint": "addresses",
            "transaction_endpoint": "transactions",
            "decimals": 6  # USDT обычно имеет 6 знаков после запятой
        },
        "bsc": {
            "base_url": "https://beta.chaingateway.io/api/v2/bsc",
            "usdt_contract": "0x55d398326f99059fF775485246999027B3197955",
            "balance_endpoint": "balances/{address}/bep20/{contract}",
            "address_endpoint": "addresses",
            "transaction_endpoint": "transactions",
            "decimals": 18 # Иногда USDT на BSC указывается с 18 decimals в API, проверьте документацию
        },
        "tron": {
            "base_url": "https://beta.chaingateway.io/api/v2/tron",
            "usdt_contract": "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj",
            "balance_endpoint": "balances/{address}/trc20/{contract}",
            "address_endpoint": "addresses",
            "transaction_endpoint": "transactions",
            "decimals": 6
        }
    }

    @staticmethod
    async def create_address(headers: Dict[str, str], network: str, password: str = "strongpassword") -> str:
        """
        Создать новый адрес для выбранной сети (ethereum, bsc, tron).
        """
        config = USDTAPI.NETWORK_CONFIG[network]
        url = f"{config['base_url']}/{config['address_endpoint']}"
        payload = {"password": password}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status not in (200, 201):
                    raise Exception(f"Ошибка при создании адреса: {response.status}, {await response.text()}")
                data = await response.json()
                # Проверяем структуру ответа. Для Ethereum и Tron ранее возвращалось что-то типа data["data"][0]["address"] или data["data"]["address"]
                # Для BSC - аналогично. Возможно потребуется адаптировать под конкретную сеть.
                # Ниже - общий пример. Проверяйте структуру ответа для каждой сети!

                # Пример для Ethereum (ранее было data["data"]["adderess"]):
                # Пример для Tron (data["data"][0]["address"])
                # Пример для BSC (data["data"]["bscaddress"])

                # Попытка универсально разобрать:
                d = data.get("data", {})
                # Случай Tron (список)
                if isinstance(d, list) and len(d) > 0 and "address" in d[0]:
                    return d[0]["address"]
                # Случай Ethereum (data["data"]["adderess"])
                if "adderess" in d:  # опечатка в документе, возможно address
                    return d["adderess"]
                # Случай BSC (data["data"]["bscaddress"])
                if "bscaddress" in d:
                    return d["bscaddress"]
                # Случай Tron/Ethereum если address напрямую
                if "address" in d:
                    return d["address"]
                
                raise Exception("Не удалось найти адрес в ответе API")

    @staticmethod
    async def get_balance(headers: Dict[str, str], network: str, address: str) -> float:
        """
        Получить баланс USDT на указанном адресе в выбранной сети.
        """
        config = USDTAPI.NETWORK_CONFIG[network]
        url = f"{config['base_url']}/{config['balance_endpoint'].format(address=address, contract=config['usdt_contract'])}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Ошибка при получении баланса: {response.status}, {await response.text()}")
                data = await response.json()
                # Проверяем структуру ответа.
                # Для Ethereum/BSC: data["data"] может быть строка с числом баланса. USDT обычно возвращается с decimals.
                # Для Tron: может быть объект с "balance".

                # Попытка универсального разбора.
                balance_data = data.get("data", {})
                # Если это строка - возможно это сразу баланс:
                if isinstance(balance_data, str):
                    # Баланс возвращается в "человеческом" формате, скорей всего уже с учётом decimals.
                    return float(balance_data)
                # Если это dict с полем "balance"
                if isinstance(balance_data, dict) and "balance" in balance_data:
                    return float(balance_data["balance"])

                # Если структура иная - нужно адаптировать под конкретный ответ.
                raise Exception("Не удалось определить баланс из ответа API")

    @staticmethod
    async def create_transaction(
        headers: Dict[str, str],
        network: str,
        private_key: str,
        from_address: str,
        to_address: str,
        amount_usdt: float,
        password: str = None,
        # Параметры газа и пр. можно добавлять опционально
    ) -> Any:
        """
        Создать транзакцию для перевода USDT в выбранной сети.
        Для Ethereum/BSC (ERC20/BEP20):
          - Нужно указать contract_address в payload,
          - amount в минимальных единицах (Wei для ETH, но у USDT 6/18 decimals, значит надо умножить).
        Для Tron (TRC20):
          - Транзакция создаётся через TriggerSmartContract. Проверяйте документацию Chaingateway для TRC20 отправок.
        
        Ниже приведён общий пример, который может потребовать корректировки.
        """

        config = USDTAPI.NETWORK_CONFIG[network]
        url = f"{config['base_url']}/{config['transaction_endpoint']}"

        decimals = config['decimals']
        # Конвертация в минимальные единицы (например, для USDT с 6 decimals: amount_usdt * 10^6)
        amount_units = int(amount_usdt * (10 ** decimals))

        # Пример для Ethereum / BSC (ERC20/BEP20):
        # Обычно payload для отправки токенов через Chaingateway API включает:
        # - from
        # - to
        # - contract_address
        # - amount (в минимальных единицах)
        # - privatekey или password
        # - Возможно, gas, gasprice и т.д.
        # Проверяйте документацию для точного формата.

        # Для Tron (TRC20) отправка может выглядеть иначе:
        # Возможно, просто указать "privatekey", "to", "contract_address", "amount" и т.д.
        # См. документацию Chaingateway.

        # Ниже - пример для Ethereum/BSC ERC20 транзакций:
        if network in ["ethereum", "bsc"]:
            payload = {
                "from": from_address,
                "to": to_address,
                "contract_address": config['usdt_contract'],
                "amount": str(amount_units),
                "privatekey": private_key
                # Можно добавить gas, gasprice, maxFeePerGas, maxPriorityFeePerGas при необходимости
            }
            if password:
                payload["password"] = password

        elif network == "tron":
            # Для TRC20 нужно использовать TriggerSmartContract,
            # Однако Chaingateway упрощает это. Согласно документации,
            # для TRC20 транзакции можно указать "contract_address" и "amount",
            # и она сама вызовет контракт. Проверяйте актуальную доку.
            payload = {
                "from": from_address,
                "to": to_address,
                "amount": amount_usdt,  # возможно, для Tron указывать в нормальном формате, проверяйте доку
                "privatekey": private_key,
                "contract_address": config['usdt_contract']
            }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status not in (200, 201):
                    raise Exception(f"Ошибка при создании транзакции: {response.status}, {await response.text()}")
                data = await response.json()
                return data
