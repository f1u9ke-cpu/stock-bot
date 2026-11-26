import requests
from bs4 import BeautifulSoup
import time
import os

# 要爬的股票
stock = ["1101", "2330"]

# Telegram 機器人金鑰
token = os.environ["BOT_TOKEN"]
chat_id = os.environ["CHAT_ID"]

# 迴圈依序爬股價
for i in range(len(stock)):
    stockid = stock[i]

    # 股票網址
    url = "https://tw.stock.yahoo.com/quote/" + stockid + ".TW"

    # 發送請求
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()

    # 解析 HTML
    soup = BeautifulSoup(r.text, "html.parser")

    # 定位股價
    price_tag = soup.select_one(
        'span[class*="Fz(32px)"][class*="Fw(b)"][class*="Mend(16px)"]'
    )

    if price_tag:
        price = price_tag.get_text(strip=True)
        message = "股票 " + stockid + " 最新股價為 " + price
    else:
        message = "股票 " + stockid + " 無法取得股價"

    # Telegram 發送訊息
    api_url = f"https://api.telegram.org/bot{token}/sendMessage"

    response = requests.post(api_url, data={
        "chat_id": chat_id,
        "text": message
    }, timeout=30)

    if not response.ok:
        raise RuntimeError("Telegram 發送失敗")

    time.sleep(3)
