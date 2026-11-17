from project import parse_trade, next_delay, init_db


def test_parse_trade():
    raw = '{"e":"trade","E":1794643117119,"s":"BTCUSDT","t":6853228070,"p":"67174.08000000","q":"0.00018000","T":1794643117119,"m":true,"M":true}'
    result = parse_trade(raw)
    assert result['trade_id'] == 6853228070
    assert result['price'] == 67174.08000000
    assert result['quantity'] == 0.00018000
    assert result['symbol'] == 'BTCUSDT'
    assert result['trade_time_ms'] == 1794643117119
    assert result['is_buyer_maker'] == True


def test_next_delay():
    assert next_delay(0) == 1
    assert next_delay(3) == 8
    assert next_delay(7) == 60


def test_init():
    conn = init_db(":memory:")   
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    assert ("trades",) in rows


