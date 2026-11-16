from project import parse_trade 
from project import next_delay


def test_parse_trade():
    raw ='{"e":"trade","E":1794643117119,"s":"BTCUSDT","t":6853228070,"p":"67174.08000000","q":"0.00018000","T":1794643117119,"m":true,"M":true}' # วางข้อความจริง 1 ตัวที่คุณคัดลอกจาก Step 1 (ใน quote เดี่ยว)
    result = parse_trade(raw)
    assert result["trade_id"] == 6853228070
    assert result["price"] == 67174.08000000
    assert result["quantity"] == 0.00018000
    assert result["symbol"] == "BTCUSDT"


def test_next_delay():
    assert next_delay(0) == 1
    assert next_delay(3) == 8
    assert next_delay(7) == 60

