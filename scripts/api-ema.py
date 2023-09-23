from flask import Flask, request, jsonify, render_template
from datetime import date, timedelta
from jugaad_data.nse import stock_df

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def calculate_ema(df, column_name, window):
    ema_series = df[column_name].ewm(span=window, adjust=False).mean()
    return ema_series

def check_red_alert(symbol, ema_window=100):
    df = stock_df(symbol=symbol, from_date=date.today() - timedelta(days=30*7),
                  to_date=date.today(), series="EQ")
    df = df.iloc[::-1]

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
            return f"Yellow Alert for {symbol}: 20 Weekly EMA closing on LTP, less than 5% away!"
    
    return f"No Alert for {symbol}."

@app.route('/red-alert', methods=['POST'])
def red_alert():
    data = request.get_json()
    symbols = data.get('symbols', [])
    ema_window = data.get('ema_window', 100)

    alerts = {}
    for symbol in symbols:
        alert = check_red_alert(symbol, ema_window)
        if alert:
            alerts[symbol] = alert

    return jsonify(alerts)

if __name__ == "__main__":
    app.run(debug=True)
