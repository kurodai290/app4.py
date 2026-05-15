<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>最強経営シミュレーター</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; padding: 20px; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
        .stat { font-size: 1.2em; margin: 10px 0; border-bottom: 1px solid #eee; padding-bottom: 5px; }
        button { width: 100%; padding: 10px; margin: 5px 0; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 5px; }
        button:disabled { background: #ccc; }
        #log { font-size: 0.9em; color: #555; background: #e9ecef; padding: 10px; height: 100px; overflow-y: auto; margin-top: 10px; }
    </style>
</head>
<body>

<div class="card">
    <h2>🏢 会社経営シミュレーター</h2>
    <div class="stat">資産: <span id="money">0</span>円</div>
    <div class="stat">シェア: <span id="share">5</span>% | 従業員: <span id="staff">0</span>人</div>
    <div id="ipo-badge" style="display:none; color: gold; font-weight: bold;">★上場企業★</div>

    <button onclick="work()">1: 営業活動 (自力で稼ぐ)</button>
    <button onclick="hire()">2: 社員を雇う (1,000円)</button>
    <button onclick="develop()">3: 新商品開発 (5,000円)</button>
    <button id="ipo-btn" onclick="ipo()">4: 株式上場 (条件: 5万/シェア30%)</button>
    <button onclick="loan()" style="background: #6c757d;">5: 銀行融資 (10,000円借入)</button>

    <div id="log">ゲーム開始！まずは営業活動で資金を貯めましょう。</div>
</div>

<script>
    let money = 2000;
    let share = 5;
    let staff = 0;
    let isListed = false;
    let debt = 0;

    function updateDisplay() {
        document.getElementById('money').innerText = money.toLocaleString();
        document.getElementById('share').innerText = share;
        document.getElementById('staff').innerText = staff;
        document.getElementById('ipo-btn').disabled = (money < 50000 || share < 30 || isListed);
        if(isListed) document.getElementById('ipo-badge').style.display = 'block';
    }

    function addLog(msg) {
        const log = document.getElementById('log');
        log.innerHTML = msg + "<br>" + log.innerHTML;
    }

    // 1秒ごとに収益発生
    setInterval(() => {
        let income = staff * 100 * (1 + share/100);
        let tax = income > 0 ? Math.floor(income * 0.3) : 0;
        let profit = Math.floor(income - tax);
        money += profit;
        updateDisplay();
    }, 1000);

    function work() {
        money += 100;
        addLog("営業活動で100円稼ぎました。");
        updateDisplay();
    }

    function hire() {
        if (money >= 1000) {
            money -= 1000;
            staff++;
            addLog("平社員を採用しました！");
            updateDisplay();
        } else { addLog("資金が足りません。"); }
    }

    function develop() {
        if (money >= 5000) {
            money -= 5000;
            let plus = Math.floor(Math.random() * 10);
            share += plus;
            addLog(`新商品を開発！シェアが ${plus}% 上がりました。`);
            updateDisplay();
        } else { addLog("資金が足りません。"); }
    }

    function ipo() {
        isListed = true;
        money += 200000;
        addLog("祝・上場！200,000円の資金を調達しました！");
        updateDisplay();
    }

    function loan() {
        money += 10000;
        debt += 12000;
        addLog("銀行から10,000円借りました。返済は自動で行われます。");
        updateDisplay();
    }

    updateDisplay();
</script>
</body>
</html>
