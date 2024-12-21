import asyncio
import firebase_admin
from firebase_admin import credentials, db
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from back.API.BTCAPI import BitcoinAPI as btc
from back.API import BNBAPI as bnb
from back.API.ETHAPI import EthereumAPI as eth
from back.API.TRONAPI import TronAPI as tron
from back.API.USDTAPI import USDTAPI as usdt
from telebot import types
API_TOKEN = '7525977443:AAF7F-CdF6VNmerkrpeE6MrFFflZPLClZeg'
cred = credentials.Certificate('service.json')
headers = {
        "Authorization": "Bearer jPNgM8aIo2NmXOxRMyAtlnBW89im9g5KwMWvA1lPf2a12985",  
        "Content-Type": "application/json"
}
# Инициализация приложения Firebase с указанием URL вашей Realtime Database
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crypto-ac75d-default-rtdb.europe-west1.firebasedatabase.app/'
})


database = db.reference()
bot = AsyncTeleBot(API_TOKEN)
def fetch_user_by_id(user_id,path):
    
    ref = db.reference(f'users/{user_id}/{path}')  # Укажите путь к данным
    user_data = ref.get()
    return user_data

# Обработчик команды /start
@bot.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await bot.reply_to(message, "Hello," + message.from_user.full_name)
    
    ref = db.reference(f"users/{message.chat.id}")
    data = ref.get()
    if data is None:
        btc_address = await btc.create_wallet(headers,"123")
        eth_address = await eth.create_address(headers,"123")
        bsc_address = await bnb.create_address(headers)
        trx_address = await tron.create_address(headers)
        usdt_trx_address = await tron.create_address(headers)
        usdt_eth_address = await eth.create_address(headers,"123")
        usdt_btc_address = await bnb.create_address(headers,"123")
        ref.set({
            "btc_address":btc_address,
            "bsc_address":bsc_address,
            "trx_address":trx_address[0],
            "trx_address_privatekey":trx_address[1],
            "eth_address":eth_address,
            "usdt_trx_address":usdt_trx_address[0],
            "usdt_trx_address_privatekey":usdt_trx_address[1],
            "usdt_eth_address":usdt_eth_address,
            "usdt_btc_address":usdt_btc_address,


        })
        await bot.send_message(message.chat.id, "Вот ссылка")
    btc_address=fetch_user_by_id(message.chat.id,"btc_address")
    eth_address=fetch_user_by_id(message.chat.id,"eth_address")
    bsc_address=fetch_user_by_id(message.chat.id,"bsc_address")
    trx_address=fetch_user_by_id(message.chat.id,"trx_address")
    usdt_trx_address=fetch_user_by_id(message.chat.id,"usdt_trx_address")
    usdt_eth_address=fetch_user_by_id(message.chat.id,"usdt_eth_address")
    usdt_btc_address=fetch_user_by_id(message.chat.id,"usdt_btc_address")
    print(btc_address,eth_address,bsc_address,trx_address,usdt_trx_address,usdt_eth_address,usdt_btc_address,)    
    btc_balance = await btc.get_balance(headers,btc_address)
    eth_balance = await eth.get_balance(headers,eth_address)
    bsc_balance = await bnb.get_balance(headers,bsc_address)
    trx_balance = await tron.get_balance(headers,trx_address)
    usdt_trx_balance = await tron.get_balance(headers,usdt_trx_address)
    usdt_eth_balance = await eth.get_balance(headers,usdt_eth_address)
    usdt_btc_balance = await btc.get_balance(headers,usdt_btc_address)
    ref.update({
"btc_balance":btc_balance,
"eth_balance":eth_balance,
"bsc_balance":bsc_balance,
"trx_balance":trx_balance,
"usdt_trx_balance":usdt_trx_balance,
"usdt_eth_balance":usdt_eth_balance,
"usdt_btc_balance":usdt_btc_balance
        })
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Перейти на сайт", url="https://finecpay.com/")
    keyboard.add(button)
    await bot.send_message(
        chat_id=message.chat.id, 
        text="Open wallet:", 
        reply_markup=keyboard
    )

async def main():
    await bot.infinity_polling()

if __name__ == '__main__':
    asyncio.run(main())
