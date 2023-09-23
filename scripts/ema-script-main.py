from datetime import date, timedelta
from jugaad_data.nse import stock_df


def calculate_ema(df, column_name, window):
    ema_series = df[column_name].ewm(span=window, adjust=False).mean()
    return ema_series

def check_red_alert(symbol, ema_window=100):
    df = stock_df(symbol=symbol, from_date=date.today() - timedelta(days=30*7),
                  to_date=date.today(), series="EQ")
    df = df.iloc[::-1]
    print(df)

    # Calculate EMA
    ema_series = calculate_ema(df, 'CLOSE', ema_window)

    # Check for Red Alert
    if not ema_series.empty:
        print(ema_series)
        current_ema = ema_series.iloc[-1]
        previous_ema = ema_series.iloc[-2] if len(ema_series) >= 2 else ema_series.iloc[-1]
        current_price = df['CLOSE'].iloc[-1]

        if current_ema > current_price:
            return f"Red Alert for {symbol}: 20 Weekly EMA Crossed LTP!"
        elif (current_price - current_ema)/current_ema <  0.05:
            return f"Yellow Alert for {symbol}: 20 Weekly EMA closing on LTP!"
    
    return f"No Alert for {symbol}."

def main():
    symbols = input("Enter symbols separated by spaces: ").split()
    ema_window = 100  # You can adjust the EMA window as needed

    for symbol in symbols:
        result = check_red_alert(symbol, ema_window)
        print(result)

if __name__ == "__main__":
    main()
