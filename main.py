!pip install -q ccxt requests pytz

import ccxt
import requests
import time
from datetime import datetime
import pytz

# ==========================================
# 1. 配置 Telegram 機器人參數
# ==========================================
TELEGRAM_BOT_TOKEN = "8655643780:AAH5602Z6WvWjr73U-eNyewkSLais-BDWaE"
TELEGRAM_CHAT_ID = "8688428406"

# 香港時區設定
hk_tz = pytz.timezone('Asia/Hong_Kong')

def send_telegram_alert(message):
    """發送即時訊息至你的 Telegram 並印出 API 回傳狀態"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        res_data = response.json()
        if not res_data.get("ok"):
            print(f"⚠️ Telegram 發送失敗，錯誤原因: {res_data}")
        else:
            print("✅ Telegram 訊息成功送出！")
    except Exception as e:
        print(f"❌ Telegram 連線異常: {e}")

# ==========================================
# 2. 初始化交易所
# ==========================================
binance = ccxt.binance({'enableRateLimit': True})
okx = ccxt.okx({'enableRateLimit': True})

SYMBOL_LIST = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'DOGE/USDT', 'PEPE/USDT', 'XRP/USDT', 'BNB/USDT']
MIN_NET_PROFIT_THRESHOLD = 0.003 
SIMULATED_CAPITAL = 1000 

print("🚀 [STAGE 3 AGENT] 零風險 Telegram 模擬套利 Bot 正式啟動 (香港時間版)...")

# 立即測試發送第一條訊息
test_time = datetime.now(hk_tz).strftime('%Y-%m-%d %H:%M:%S')
send_telegram_alert(f"🤖 *[System Console]* 你的 Crypto 模擬套利 Agent 已上線！\n⏱️ 當前香港時間: `{test_time}`\n正為你 24/7 掃描市場價差 Glitch...")

def run_paper_trading_loop():
    while True:
        timestamp = datetime.now(hk_tz).strftime('%Y-%m-%d %H:%M:%S')
        print(f"🔍 [{timestamp}] 正在掃描市場價差...")
        
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
                    print(f"\n⚡ 觸發套利機會！{symbol} 淨利: {net_profit_1 * 100:.3f}%")
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
                    print(f"\n⚡ 觸發套利機會！{symbol} 淨利: {net_profit_2 * 100:.3f}%")
                    send_telegram_alert(alert_msg)
                    time.sleep(5)  

            except Exception as e:
                pass
        
        time.sleep(10)

run_paper_trading_loop()
