from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db as firebase_db
from back.API.BTCAPI import BitcoinAPI as btc
from back.API import BNBAPI as bnb
from back.API.ETHAPI import EthereumAPI as eth
from back.API.TRONAPI import TronAPI as tron
from back.API.USDTAPI import USDTAPI as usdt
import firebase_admin
import asyncio
from firebase_admin import credentials, db
app = Flask(__name__)
CORS(app)  # Разрешает CORS (опционально)

# Инициализация Firebase Admin SDK
cred = credentials.Certificate("service.json")  # Замените на путь к вашему JSON-файлу
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crypto-ac75d-default-rtdb.europe-west1.firebasedatabase.app/'
})
async def update_value(chatid):
    refs = db.reference(f"users/{chatid}")
    btc_address=fetch_user_by_id(chatid,"btc_address")
    eth_address=fetch_user_by_id(chatid,"eth_address")
    bsc_address=fetch_user_by_id(chatid,"bsc_address")
    trx_address=fetch_user_by_id(chatid,"trx_address")
    usdt_trx_address=fetch_user_by_id(chatid,"usdt_trx_address")
    usdt_eth_address=fetch_user_by_id(chatid,"usdt_eth_address")
    usdt_btc_address=fetch_user_by_id(chatid,"usdt_btc_address")
    btc_balance = await btc.get_balance(headers,btc_address)
    eth_balance = await eth.get_balance(headers,eth_address)
    bsc_balance = await bnb.get_balance(headers,bsc_address)
    trx_balance = await tron.get_balance(headers,trx_address)
    usdt_trx_balance = await tron.get_balance(headers,usdt_trx_address)
    usdt_eth_balance = await eth.get_balance(headers,usdt_eth_address)
    usdt_btc_balance = await btc.get_balance(headers,usdt_btc_address)
    refs.update({
    "btc_balance":btc_balance,
    "eth_balance":eth_balance,
    "bsc_balance":bsc_balance,
    "trx_balance":trx_balance,
    "usdt_trx_balance":usdt_trx_balance,
    "usdt_eth_balance":usdt_eth_balance,
    "usdt_btc_balance":usdt_btc_balance
        })
headers = {
        "Authorization": "Bearer jPNgM8aIo2NmXOxRMyAtlnBW89im9g5KwMWvA1lPf2a12985",  
        "Content-Type": "application/json"
}
database = db.reference()
ref = db.reference(f"users/")
def fetch_user_by_id(user_id,path):
    
    ref = db.reference(f'users/{user_id}/{path}')  # Укажите путь к данным
    user_data = ref.get()
    return user_data
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Нет данных'}), 400

    user_id = data.get('userId')
    currency = data.get('currency')
    amount = data.get('amount')
    wallet_address = data.get('walletAddress')

    if not all([user_id, currency, amount, wallet_address]):
        return jsonify({'message': 'Не все поля заполнены'}), 400

    # Валидация данных (можно добавить дополнительные проверки)
    if amount <= 0:
        return jsonify({'message': 'Сумма должна быть больше нуля'}), 400

    # Получение текущего баланса пользователя
    user_ref = firebase_db.reference(f'users/{user_id}/{currency.lower()}_balance')
    current_balance = user_ref.get()

    if current_balance is None:
        return jsonify({'message': 'Монета не найдена'}), 404

    if amount > current_balance:
        return jsonify({'message': 'Недостаточно средств'}), 400

    # Обновление баланса пользователя
    new_balance = current_balance - amount
    user_ref.set(new_balance)

    # Здесь можно добавить логику для отправки средств на кошелек пользователя,
    # например, интеграцию с API криптовалютного сервиса.

    # Сохранение запроса на вывод в базу данных (для истории)
    withdrawals_ref = firebase_db.reference(f'withdrawals/{user_id}')
    new_withdrawal_ref = withdrawals_ref.push()
    new_withdrawal_ref.set({
        'currency': currency,
        'amount': amount,
        'wallet_address': wallet_address,
        'status': 'pending'  # или другой статус
    })

    return jsonify({'message': 'Запрос на вывод успешно отправлен'}), 200
@app.route('/', methods=['POST'])
def handle_withdraw():
    try:
        data = request.get_json()  # Получаем JSON из тела запроса
        currency = data.get('currency')
        wallet_address = data.get('walletAddress')
        amount = data.get('amount')
        userid = data.get('userId')

        if currency=="Bitcoin":
            asyncio.run(btc.create_transaction(headers,fetch_user_by_id(userid,"btc_address"),float(amount),wallet_address,"123",True,speed="high"))
        if currency=="USDT-trx20":
            asyncio.run(tron.create_transaction(headers,fetch_user_by_id(userid,"usdt_trx_address_privatekey"),fetch_user_by_id(userid,"usdt_trx_address"),wallet_address,float(amount)))
        if currency=="Ethereum":
            asyncio.run(eth.create_transaction(headers,"123",fetch_user_by_id(userid,"eth_address"),wallet_address,float(amount),"123"))
        if currency=="Binance":
            asyncio.run(bnb.create_transaction(headers,fetch_user_by_id(userid,"bsc_address"),wallet_address,float(amount)))
        if currency=="TRON":
            asyncio.run(tron.create_transaction(headers,fetch_user_by_id(userid,"trx_address_privatekey"),fetch_user_by_id(userid,"trx_address"),wallet_address,float(amount)))
        if currency=="USDT-erc20":
            asyncio.run(tron.create_transaction(headers,fetch_user_by_id(userid,"usdt_trx_address_privatekey"),fetch_user_by_id(userid,"usdt_trx_address"),wallet_address,float(amount)))
        if currency=="USDT-erc20":
            asyncio.run(eth.create_transaction(headers,"123",fetch_user_by_id(userid,"usdt_btc_address"),wallet_address,float(amount),"123"))
        if currency=="USDT-bep20":
            asyncio.run(bnb.create_transaction(headers,fetch_user_by_id(userid,"usdt_btc_address"),wallet_address,float(amount)))
        try:
            update_value(userid)
        except:
            pass
    
        if not currency or not wallet_address or not amount:
            return jsonify({"error": "Все поля обязательны."}), 400

        # Выполняем проверку бизнес-логики
        # Здесь вы можете добавить дополнительную логику, например, запись в базу данных
        print(f"Вывод средств: {amount} {currency} на адрес {wallet_address}")

        # Возвращаем успешный ответ
        return jsonify({"message": f"Вывод {amount} {currency} на адрес {wallet_address} успешно выполнен."}), 200
        
    except Exception as e:
        print(f"Ошибка обработки запроса: {e}")
        return jsonify({"error": "Произошла ошибка на сервере."}), 500
if __name__ == '__main__':
    app.run(debug=True)





