!pip install -q ccxt requests pytz flask

import ccxt
import requests
import time
from datetime import datetime
import pytz
import threading
from flask import Flask

# ==========================================
# 0. 免費 Web 伺服器 (讓 Render Web Service 識別)
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7 in background!"

def run_flask():
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# 1. 配置 Telegram 機器人參數
# ==========================================
TELEGRAM_BOT_TOKEN = "8655643780:AAH5602Z6WvWjr73U-eNyewkSLais-BDWaE"
TELEGRAM_CHAT_ID = "8688428406"

hk_tz = pytz.timezone('Asia/Hong_Kong')

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram 連線異常: {e}")

# ==========================================
# 2. 核心監控邏輯
# ==========================================
binance = ccxt.binance({'enableRateLimit': True})
okx = ccxt.okx({'enableRateLimit': True})

SYMBOL_LIST = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'DOGE/USDT', 'PEPE/USDT', 'XRP/USDT', 'BNB/USDT']
MIN_NET_PROFIT_THRESHOLD = 0.003 
SIMULATED_CAPITAL = 1000 

def run_paper_trading_loop():
    print("🚀 [STAGE 3 AGENT] 24/7 免費雲端 Bot 啟動成功...")
    test_time = datetime.now(hk_tz).strftime('%Y-%m-%d %H:%M:%S')
    send_telegram_alert(f"🤖 *[System Console]* 你的 24/7 免費雲端 Bot 已成功部署至 Render！\n⏱️ 香港時間: `{test_time}`\n正全天候監控市場價差...")

    while True:
        timestamp = datetime.now(hk_tz).strftime('%Y-%m-%d %H:%M:%S')
        for symbol in SYMBOL_LIST:
            try:
                ticker_a = binance.fetch_ticker(symbol)
                ticker_b = okx.fetch_ticker(symbol)
                
                ask_a = ticker_a['ask']  
                bid_b = ticker_b['bid']  
                ask_b = ticker_b['ask']  
                bid_a = ticker_a['bid']  

                spread_1 = (bid_b - ask_a) / ask_a  
                spread_2 = (bid_a - ask_b) / ask_b  

                ESTIMATED_FEE = 0.002
                net_profit_1 = spread_1 - ESTIMATED_FEE
                net_profit_2 = spread_2 - ESTIMATED_FEE

                if net_profit_1 > MIN_NET_PROFIT_THRESHOLD:
                    estimated_cash_earned = SIMULATED_CAPITAL * net_profit_1
                    alert_msg = (
                        f"💰 *[!] 發現零風險套利 Glitch！*\n\n"
                        f"🔹 *交易對:* `{symbol}`\n"
                        f"🔹 *操作路徑:* Binance 買入 (`${ask_a}`) ➔ OKX 賣出 (`${bid_b}`)\n"
                        f"📈 *原始價差:* `{spread_1 * 100:.3f}%`\n"
                        f"💸 *扣除手續費後淨利:* `{net_profit_1 * 100:.3f}%`\n"
                        f"💵 *假設 $1000 本金預計純利:* `+${estimated_cash_earned:.2f} USDT`\n\n"
                        f"⏱️ _時間: {timestamp} (Paper Trading 模擬成交)_"
                    )
                    send_telegram_alert(alert_msg)
                    time.sleep(5)  

                elif net_profit_2 > MIN_NET_PROFIT_THRESHOLD:
                    estimated_cash_earned = SIMULATED_CAPITAL * net_profit_2
                    alert_msg = (
                        f"💰 *[!] 發現零風險套利 Glitch！*\n\n"
                        f"🔹 *交易對:* `{symbol}`\n"
                        f"🔹 *操作路徑:* OKX 買入 (`${ask_b}`) ➔ Binance 賣出 (`${bid_a}`)\n"
                        f"📈 *原始價差:* `{spread_2 * 100:.3f}%`\n"
                        f"💸 *扣除手續費後淨利:* `{net_profit_2 * 100:.3f}%`\n"
                        f"💵 *假設 $1000 本金預計純利:* `+${estimated_cash_earned:.2f} USDT`\n\n"
                        f"⏱️ _時間: {timestamp} (Paper Trading 模擬成交)_"
                    )
                    send_telegram_alert(alert_msg)
                    time.sleep(5)  

            except Exception as e:
                pass
        
        time.sleep(10)

# 開啟多線程：一邊跑網頁伺服器，一邊跑監控 Bot
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_paper_trading_loop()
