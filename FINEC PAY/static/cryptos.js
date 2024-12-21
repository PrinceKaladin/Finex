const userId = getTelegramUserId(); 
function fetchUserById1(userId,path) {
  const userRef = db.ref(`users/${userId}/${path}`);
  const snapshot = userRef.once('value');
  console.log(snapshot.val())
  return snapshot.val();
}
function showDepositModal() {
  const modal = document.getElementById('depositModal');
  if (modal) {
    modal.style.display = 'block';

    const depositCoinSelect = document.getElementById('depositCoin');
    depositCoinSelect.removeEventListener('change', fetchDepositAddress);
    depositCoinSelect.addEventListener('change', fetchDepositAddress);
    fetchDepositAddress(); 
  }
}
async function fetchUserById1(userId, path) {
  try {
    const userRef = db.ref(`users/${userId}/${path}`);
    const snapshot = await userRef.once('value');
    return snapshot.val();
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
    return null;
  }
}

function closeDepositModal() {
  const modal = document.getElementById('depositModal');
  if (modal) {
    modal.style.display = 'none';
  }
}

async function fetchDepositAddress() {
  const selectedCoin = document.getElementById('depositCoin').value;
  const addressSpan = document.getElementById('depositAddress');

  const warningCoinSpans = document.querySelectorAll('#selectedCoin, .selected-coin');

  const coinFieldMapping = {
    USDT: 'usdt_eth_address',
    BTC: 'btc_address',
    ETH: 'eth_address',
    TRON: 'trx_address',
    'USDT-trx20': 'usdt_trx_address',
    'USDT-erc20': 'usdt_eth_address',
    'USDT-bep20': 'bsc_address'
  };

  const fieldName = coinFieldMapping[selectedCoin];

   

    
      const address = await fetchUserById1(userId,fieldName)
      console.log(address)
      if (address) {
        addressSpan.textContent = address;


        warningCoinSpans.forEach(span => {
          span.textContent = selectedCoin;
        });
      
}}



// Копировать адрес депозита в буфер обмена
function copyAddress() {
  const address = document.getElementById('depositAddress').textContent;
  navigator.clipboard.writeText(address)
    .then(() => {
      alert('Адрес скопирован в буфер обмена!');
    })
    .catch(err => {
      console.error('Error copying to clipboard:', err);
    });
}

// Добавить обработчики событий после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('.close-modal').addEventListener('click', closeDepositModal);
  document.getElementById('depositCoin').addEventListener('change', fetchDepositAddress);
});
