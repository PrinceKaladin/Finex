
import asyncio
from BTCAPI import BitcoinAPI as btc
import BNBAPI as bnb
from ETHAPI import EthereumAPI as eth
from TRONAPI import TronAPI as tron
from USDTAPI import USDTAPI as usdt
headers = {
        "Authorization": "Bearer jPNgM8aIo2NmXOxRMyAtlnBW89im9g5KwMWvA1lPf2a12985",  
        "Content-Type": "application/json"
}
a = asyncio.run(bnb.get_balance(headers,"0xe6f7b49FC82CBb271f573FED40aE0255E6e2733b"))
async def send_welcome():
   btc_address = await btc.get_balance(headers,"lJHRz1taxDI44N7d4FTGNOxB1Fs2Q8")
   eth_address = await eth.get_balance(headers,"0xabE83dcdA13245D02AF5326B9874Ed2B42F5A583")
   bsc_address = await bnb.get_balance(headers,"0xC4C43D730513a99Fc90c35586D80b3cDA6BfeD5E")
   trx_address = await tron.get_balance(headers,"TBkx7Ztu4gtxuuezLNCqF1i3zpYs5HRBBE")
   usdt_trx_address = await usdt.get_balance(headers,"TFSRrq5bDFMJzHkrPyG24YAgkukuCCY7a4")
   #usdt_eth_address = await usdt.get_balance(headers, "ethereum", "123")
   #usdt_btc_address = await usdt.get_balance(headers, "bsc", "123")
asyncio.run(send_welcome())