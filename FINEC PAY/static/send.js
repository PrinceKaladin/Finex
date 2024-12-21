function showWithdrawModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'block';
  
    const modalContent = modal.querySelector('.modal-content');
    modalContent.innerHTML = `
      <span id="modal-close" class="close">&times;</span>
      <h2>Выберите валюту</h2>
      <select id="currency-select" class="modal-select">
        <option value="">-- Выберите валюту --</option>
      </select>
      <h2>Введите адрес кошелька</h2>
      <input type="text" id="wallet-address" class="modal-input" placeholder="Адрес кошелька">
      <h2>Введите сумму</h2>
      <input type="number" id="withdraw-amount" class="modal-input" placeholder="Сумма">
      <button id="confirm-withdraw" class="modal-btn">Подтвердить</button>
    `;
  
    const closeButton = modal.querySelector('#modal-close');
    closeButton.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  
    populateCurrencySelect();
  
    const confirmButton = modal.querySelector('#confirm-withdraw');
    confirmButton.addEventListener('click', handleWithdraw);
  }
  
  // Функция для заполнения списка валют
  async function populateCurrencySelect() {
    const userId = getTelegramUserId();
    const userCoins = await getUserCoins(userId);
    const select = document.getElementById('currency-select');
  
    userCoins.forEach(coin => {
      const option = document.createElement('option');
      option.value = coin.id;
      option.textContent = `${coin.name} - Баланс: ${coin.balance}`;
      select.appendChild(option);
    });
  }
  
  // Функция для обработки вывода средств
  async function handleWithdraw() {
    const currency = document.getElementById('currency-select').value;
    const walletAddress = document.getElementById('wallet-address').value;
    const amount = parseFloat(document.getElementById('withdraw-amount').value);
  
    if (!currency || !walletAddress || isNaN(amount) || amount <= 0) {
      alert('Пожалуйста, заполните все поля корректно.');
      return;
    }
  
    try {
      const userId = getTelegramUserId();;
      const userCoins = await getUserCoins(userId);
      const selectedCoin = userCoins.find(coin => coin.id === currency);
  
      if (!selectedCoin || amount > selectedCoin.balance) {
        alert('Недостаточно средств для вывода.');
        return;
      }
  
      // Выполнение POST-запроса на эту же страницу
      const response = await fetch(window.location.href, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          currency,
          walletAddress,
          amount,
          userId
        }),
      });
  
      if (!response.ok) {
        throw new Error('Ошибка сервера');
      }
     
      alert(`Вывод средств ${amount} ${selectedCoin.name} на адрес ${walletAddress} успешно выполнен.`);
      window.location.reload()
      // Закрываем модальное окно
      document.getElementById('modal').style.display = 'none';
    } catch (error) {
      console.error('Ошибка вывода средств:', error);
      alert('Произошла ошибка. Попробуйте снова позже.');
    }
  }
  