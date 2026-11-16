from project import parse_trade


def test_parse_trade():
    raw ='{"e":"trade","E":1794643117119,"s":"BTCUSDT","t":6853228070,"p":"67174.08000000","q":"0.00018000","T":1794643117119,"m":true,"M":true}' # วางข้อความจริง 1 ตัวที่คุณคัดลอกจาก Step 1 (ใน quote เดี่ยว)
    result = parse_trade(raw)
    assert result["trade_id"] == 6853228070
    assert result["price"] == 67174.08000000
    assert result["quantity"] == 0.00018000
    assert result["symbol"] == "BTCUSDT"
