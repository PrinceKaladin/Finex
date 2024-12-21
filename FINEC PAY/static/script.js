 const firebaseConfig = {
      apiKey: "AIzaSyBwqNhXYRZpTjNA91abKe_3zbAzfmxF5uY",
      authDomain: "crypto-ac75d.firebaseapp.com",
      databaseURL: "https://crypto-ac75d-default-rtdb.europe-west1.firebasedatabase.app",
      projectId: "crypto-ac75d",
      storageBucket: "crypto-ac75d.firebasestorage.app",
      messagingSenderId: "1999689198",
      appId: "1:1999689198:web:709dc30c19058538e02aff",
      measurementId: "G-QCF9YT3PKY"
    };
    const app = firebase.initializeApp(firebaseConfig);
    const db = firebase.database();

    // Fetch user data from Firebase
    async function fetchUserById(userId) {
      const userRef = db.ref(`users/${userId}`);
      const snapshot = await userRef.once('value');
      return snapshot.val();
    }

    // Get user coins
    async function getUserCoins(userId) {
      const snapshot = await fetchUserById(userId);
      if (!snapshot) throw new Error('User data not found');
      return [
        { id: 'USDT-trx20', name: 'USDT', baseId: 'tether', balance: snapshot["usdt_trx_balance"] || 0 },
        { id: 'USDT-erc20', name: 'USDT', baseId: 'tether', balance: snapshot["usdt_eth_balance"] || 0 },
        { id: 'USDT-bep20', name: 'USDT', baseId: 'tether', balance: snapshot["usdt_btc_balance"] || 0 },
        { id: 'Bitcoin', name: 'BTC', baseId: 'bitcoin', balance: snapshot["btc_balance"] || 0 },
        { id: 'Ethereum', name: 'ETH', baseId: 'ethereum', balance: snapshot["eth_balance"] || 0 },
        { id: 'Binance', name: 'BSC', baseId: 'binancecoin', balance: snapshot["bsc_balance"] || 0 },
        { id: 'TRON', name: 'TRON', baseId: 'tron', balance: snapshot["trx_balance"] || 0 },
      ];
    }

    // Fetch prices from CoinGecko
    async function fetchPrices(baseIds) {
      const url = `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=${baseIds}&sparkline=false&price_change_percentage=24h`;
      const response = await fetch(url);
      return response.json();
    }

    // Render coins data
    function renderCoins(userCoins, pricesMap) {
      const container = document.getElementById('coins');
      container.innerHTML = ''; 
      const exampleDiv = document.getElementById('total-coins')
      let rowissss=0;
      userCoins.forEach(userCoin => {
        
        const row = document.createElement('div');
        
        row.className = 'coin-row';

     

        const coinData = pricesMap[userCoin.baseId];
        const iconUrl = coinData?.image || 'https://via.placeholder.com/32';
        const coinName = userCoin.id;
        const currentPrice = coinData?.current_price || 0;
        const change24h = coinData?.price_change_percentage_24h || 0;

        row.innerHTML = `
          <div class="coin-left">
            <img class="coin-icon" src="${iconUrl}" alt="${coinName}" />
            <div class="coin-name">${coinName}</div>
          </div>
          <div class="coin-middle">
            <div class="coin-price">$${currentPrice.toFixed(2)}</div>
            <span class="coin-change ${change24h >= 0 ? 'positive' : 'negative'}">${change24h.toFixed(2)}%</span>
          </div>
          <div class="coin-right">
            <div class="coin-balance">${userCoin.balance} ${userCoin.name}</div>
            <div class="coin-balance-usd">$${(userCoin.balance * currentPrice).toFixed(2)}</div>
          </div>
        `;
        rowissss += parseFloat((userCoin.balance * currentPrice).toFixed(2));
        
        container.appendChild(row);
      });
      exampleDiv.textContent = rowissss
    }

    function getTelegramUserId() {
      if (window.Telegram && Telegram.WebApp) {
        const user = Telegram.WebApp.initDataUnsafe.user;
        if (user && user.id) {
          return user.id; // Возвращаем userId
        } else {
          console.error('Пользователь не авторизован или данных нет.');
          return null;
        }
      } else {
        console.error('Telegram WebApp SDK не загружен.');
        return null;
      }
    }
    (async () => {
      try {
        const userId = getTelegramUserId();
        const userCoins = await getUserCoins(userId);
        const uniqueBaseIds = [...new Set(userCoins.map(coin => coin.baseId))].join(',');
        const prices = await fetchPrices(uniqueBaseIds);
        const pricesMap = Object.fromEntries(prices.map(coin => [coin.id, coin]));
        renderCoins(userCoins, pricesMap);
      } catch (err) {
        console.error('Error:', err.message);
      }
    })();