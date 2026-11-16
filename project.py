import asyncio
import ssl
import certifi
import websockets
import json

URL = "wss://data-stream.binance.vision:443/ws/btcusdt@trade"

async def main():
    ctx = ssl.create_default_context(cafile=certifi.where())   
    count = 0
    async with websockets.connect(URL, ssl=ctx) as ws:       
        async for message in ws:                             
            print(parse_trade(message))                                    
            count += 1                                      
            if count >= 5:                               
                break        
                                                
def parse_trade(raw):
    data = json.loads(raw)
    return {
        "trade_id": int(data["t"]),
        "price": float(data["p"]),           
        "quantity": float(data["q"]),        
        "trade_time_ms": int(data["T"]),    
        "is_buyer_maker": data["m"],
        "symbol": data["s"],
    }


if __name__ == "__main__":
    raw = '{"e":"trade","E":1794643117119,"s":"BTCUSDT","t":6853228070,"p":"67174.08000000","q":"0.00018000","T":1794643117119,"m":true,"M":true}'
    print(parse_trade(raw))
    asyncio.run(main())