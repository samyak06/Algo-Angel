# from flask import Flask, request, jsonify
# from datetime import date, timedelta
# from jugaad_data.nse import stock_df
# from stock_indicators import indicators, Quote
# import pandas as pd

# app = Flask(__name__)

# @app.route('/stock_data', methods=['GET'])
# def get_stock_data():
#     # Get the stock symbol from the query parameters
#     stock_symbol = request.args.get('symbol')

#     if not stock_symbol:
#         return jsonify({'error': 'Stock symbol not provided'}), 400

#     try:
#         # Fetch historical stock data for the given symbol
#         df = stock_df(symbol=stock_symbol, from_date=date.today() - timedelta(days=800),
#                       to_date=date.today(), series="EQ")

#         df = df.iloc[::-1]
#         print(df)
#         # Prepare weekly OHLC data
#         # df.set_index('DATE', inplace=True)
#         # columns_to_preserve = ['OPEN', 'HIGH', 'LOW', 'CLOSE']
#         # weekly_data = {}
#         # for column in columns_to_preserve:
#         #     weekly_data[column] = df[column].resample('W').ohlc()

#         # weekly_volume = df['VOLUME'].resample('W').sum()
#         # weekly_data['VOLUME'] = weekly_volume
#         # weekly_data.reset_index(inplace=True)
#         df.set_index('DATE', inplace=True)

#         columns_to_preserve = ['OPEN', 'HIGH', 'LOW', 'CLOSE']
#         weekly_dataframes = {}
#         for column in columns_to_preserve:
#             # weekly_dataframes[column] = weekly_data
#             weekly_data = df.resample('W').apply({column: 'ohlc'})
            
#             # Reformat the columns for consistency
#             weekly_data.columns = weekly_data.columns.droplevel(0)

#         # Combine the weekly data with the weekly SMA
#         weekly_volume = df['VOLUME'].resample('W').sum()
#         weekly_data['VOLUME'] = weekly_volume
#         # Reset the index to have 'DATE' as a column
#         weekly_data.reset_index(inplace=True)

#         # Create a list of Quote objects for indicators calculation
#         quotes_list = [
#             Quote(d, o, h, l, c, v)
#             for d, o, h, l, c, v
#             in zip(weekly_data['DATE'], weekly_data['open'], weekly_data['high'], weekly_data['low'], weekly_data['close'], weekly_data['VOLUME'])
#         ]

#         # Calculate indicators (EMA, Stop, SAR)
#         ema_results = indicators.get_ema(quotes_list, 21)
#         vstop_results = indicators.get_volatility_stop(quotes_list, 20, 2.5)
#         sar_results = indicators.get_parabolic_sar(quotes_list, 0.05, 0.2, 0.02)

#         # Extract the latest values of each indicator
#         latest_ema = ema_results[-1].ema
#         latest_vstop = vstop_results[-1].sar
#         latest_sar = sar_results[-1].sar

#         # Get the most recent closing price
#         latest_close_price = df['CLOSE'].iloc[-1]

#         # Construct the response JSON
#         response_data = {
#             'stock_symbol': stock_symbol,
#             'latest_close_price': float(latest_close_price),
#             'latest_ema': float(latest_ema),
#             'latest_vstop': float(latest_vstop),
#             'latest_sar': float(latest_sar)
#         }
#         print(response_data)
#         return jsonify(response_data), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from datetime import date, timedelta
from jugaad_data.nse import stock_df
from stock_indicators import indicators, Quote
import pandas as pd
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/stock_data', methods=['POST'])  # Change the method to POST
def get_stock_data():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        print(data)
        # Check if 'symbols' key exists in the JSON data
        if 'symbols' not in data:
            return jsonify({'error': 'Stock symbols not provided'}), 400

        stock_symbols = data['symbols']  # Extract stock symbols from the JSON data

        # Create an empty list to store the response data for each stock
        response_data = []

        for stock_symbol in stock_symbols:
            # Fetch historical stock data for the given symbol
            df = stock_df(symbol=stock_symbol, from_date=date.today() - timedelta(days=700),
                          to_date=date.today(), series="EQ")

            df = df.iloc[::-1]

            # Prepare weekly OHLC data
            df.set_index('DATE', inplace=True)

            columns_to_preserve = ['OPEN', 'HIGH', 'LOW', 'CLOSE']
            weekly_dataframes = {}
            for column in columns_to_preserve:
                weekly_data = df.resample('W').apply({column: 'ohlc'})
                weekly_data.columns = weekly_data.columns.droplevel(0)

            weekly_volume = df['VOLUME'].resample('W').sum()
            weekly_data['VOLUME'] = weekly_volume
            weekly_data.reset_index(inplace=True)
            print(weekly_data)
            # Create a list of Quote objects for indicators calculation
            quotes_list = [
                Quote(d, o, h, l, c, v)
                for d, o, h, l, c, v
                in zip(weekly_data['DATE'], weekly_data['open'], weekly_data['high'], weekly_data['low'], weekly_data['close'], weekly_data['VOLUME'])
            ]
            # print(quo)
            # Calculate indicators (EMA, Stop, SAR)
            ema_results = indicators.get_ema(quotes_list, 21)
            vstop_results = indicators.get_volatility_stop(quotes_list, 20, 2.5)
            sar_results = indicators.get_parabolic_sar(quotes_list, 0.05, 0.2, 0.02)

            # Extract the latest values of each indicator
            latest_ema = ema_results[-1].ema
            latest_vstop = vstop_results[-1].sar
            latest_sar = sar_results[-1].sar

            # Get the most recent closing price
            latest_close_price = df['CLOSE'].iloc[-1]

            # Construct the response data for this stock
            stock_response_data = {
                'stock_symbol': stock_symbol,
                'latest_close_price': float(latest_close_price),
                'latest_ema': float(latest_ema),
                'latest_vstop': float(latest_vstop),
                'latest_sar': float(latest_sar)
            }

            response_data.append(stock_response_data)

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
