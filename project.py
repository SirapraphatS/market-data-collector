import asyncio
import ssl
import certifi
import websockets
import json
import sqlite3

URL = 'wss://data-stream.binance.vision:443/ws/btcusdt@trade'

def init_db(path):
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS trades (
            trade_id INTEGER PRIMARY KEY,
            price REAL,
            quantity REAL,
            trade_time_ms INTEGER,
            is_buyer_maker INTEGER,
            symbol TEXT
        )"""
    )
    conn.commit()
    return conn

def save_trade(conn, trade):
    conn.execute(
        "INSERT OR IGNORE INTO trades(trade_id, price, quantity, trade_time_ms, is_buyer_maker, symbol)  VALUES (?, ?, ?, ?, ?, ?)",
        (trade["trade_id"], trade["price"], trade["quantity"], trade["trade_time_ms"], int(trade["is_buyer_maker"]), trade["symbol"],)
    )
    conn.commit()

async def main():
    ctx = ssl.create_default_context(cafile=certifi.where())   
    conn = init_db("trades.db")
    count = 0
    async with websockets.connect(URL, ssl=ctx) as ws:       
        async for message in ws:                             
            save_trade(conn, parse_trade(message))                                    
            count += 1                                      
            if count >= 5:                               
                break       
        print(conn.execute("SELECT COUNT(*) FROM trades").fetchone())
                                                
def parse_trade(raw):
    data = json.loads(raw)
    return {
        'trade_id': int(data['t']),
        'price': float(data['p']),           
        'quantity': float(data['q']),        
        'trade_time_ms': int(data['T']),    
        'is_buyer_maker': data['m'],
        'symbol': data['s'],
    }


def next_delay(attempt):
    second = 2 ** attempt
    return min(60,second)

        


if __name__ == '__main__':
    raw = '{"e":"trade","E":1794643117119,"s":"BTCUSDT","t":6853228070,"p":"67174.08000000","q":"0.00018000","T":1794643117119,"m":true,"M":true}'
    print(parse_trade(raw))
    asyncio.run(main())