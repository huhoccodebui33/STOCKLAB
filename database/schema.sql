

CREATE TABLE IF NOT EXISTS stocks (

    id SERIAL PRIMARY KEY,

    -- Mã cổ phiếu
    symbol VARCHAR(10) UNIQUE NOT NULL,

    -- Tên công ty
    company_name VARCHAR(255),

    -- Sàn giao dịch
    exchange VARCHAR(50)

);



CREATE TABLE IF NOT EXISTS daily_prices (

    id SERIAL PRIMARY KEY,

    -- Liên kết tới bảng stocks
    stock_id INTEGER NOT NULL REFERENCES stocks(id),

    -- Ngày giao dịch
    trading_date DATE NOT NULL,

    open_price NUMERIC(12,2),

    high NUMERIC(12,2),

    low NUMERIC(12,2),

    close_price NUMERIC(12,2),

    volume BIGINT,

    -- Không cho trùng dữ liệu
    UNIQUE(stock_id, trading_date)

);