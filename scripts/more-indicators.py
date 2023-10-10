from datetime import date,timedelta
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save
from jugaad_data.nse import stock_df
from stock_indicators import indicators
from stock_indicators import Quote
import pandas as pd
import matplotlib.pyplot as plt
from stock_indicators.indicators.common.enums import CandlePart

# # def calculate_ema(df, column_name, window):
# #     # ema = df[column_name].ewm(span=window, adjust=False).mean()
# #     # return ema
# #     ema = df[column_name].ewm(span=window, adjust=False).mean()
# #     return ema.iloc[-1]

# # df = stock_df(symbol="SBIN", from_date=date.today() - timedelta(days=20),
# #             to_date=date.today(), series="EQ")

# # ema_window = 10
# # ema_20 = calculate_ema(df, 'CLOSE', ema_window)
# # print(f'EMA_20: {ema_20}')
# #   # You can adjust this to your desired EMA window
# # # df['EMA'] = calculate_ema(df, 'CLOSE', ema_window)
# # # print(df)
# # # # DST9FVJ75B5VTSNK
# # from datetime import date, timedelta
# # from jugaad_data.nse import stock_df
# # import matplotlib.pyplot as plt

# # def calculate_ema(df, column_name, window):
# #     if len(df) >= window:  # Check if there are enough data points to calculate EMA
# #         ema = df[column_name].ewm(span=window, adjust=False).mean()
# #         return ema
# #     else:
# #         return None

# def calculate_ema(df, column_name, window):
#     ema_series = df[column_name].ewm(span=window, adjust=False).mean()
#     return ema_series


# df = stock_df(symbol="DELTACORP", from_date=date.today() - timedelta(days=30*7),
#               to_date=date.today(), series="EQ")
# print(date.today())
# ema_window = 100
# df = df.iloc[::-1]
# # df.set_index('DATE', inplace=True)
# # df_weekly = df.resample('W').mean()
# filtered_df = df  # Filter rows with enough data points for EMA
# print(filtered_df)
# ema_series = calculate_ema(filtered_df, 'CLOSE', ema_window)

df = stock_df(symbol="NH", from_date=date.today() - timedelta(days=800),
              to_date=date.today(), series="EQ")

df = df.iloc[::-1]
# print(df)
# vstop_results = indicators.get_sma(quotes_list, 10)
# print(vstop_results)
# 
# vstop_results = indicators.get_volatility_stop(quotes_list, 120, 2.5)

# for r in vstop_results:
    # print(r.sar)

# Set the 'DATE' column as the DataFrame index
df.set_index('DATE', inplace=True)

columns_to_preserve = ['OPEN', 'HIGH', 'LOW', 'CLOSE']
weekly_dataframes = {}
for column in columns_to_preserve:
    # weekly_dataframes[column] = weekly_data
    weekly_data = df.resample('W').apply({column: 'ohlc'})
    
    # Reformat the columns for consistency
    weekly_data.columns = weekly_data.columns.droplevel(0)

# Combine the weekly data with the weekly SMA
weekly_volume = df['VOLUME'].resample('W').sum()
weekly_data['VOLUME'] = weekly_volume
# Reset the index to have 'DATE' as a column
weekly_data.reset_index(inplace=True)

# Print the resulting weekly data
# print(weekly_data)
# Save the DataFrame to a CSV text file
# weekly_data.to_csv('output.csv', index=False)  # Specify the filename (e.g., 'output.csv') and set index to False if you don't want to include the index

quotes_list = [
    Quote(d,o,h,l,c,v) 
    for d,o,h,l,c,v 
    in zip(weekly_data['DATE'], weekly_data['open'], weekly_data['high'], weekly_data['low'], weekly_data['close'], weekly_data['VOLUME'])
]

vstop_results = indicators.get_volatility_stop(quotes_list, 20, 2.5)
sar_results = indicators.get_parabolic_sar(quotes_list, 0.05, 0.2,0.02)
ema_results = indicators.get_ema(quotes_list,21)

latest_volatility_stop = vstop_results[-1].sar
latest_sar_results = sar_results[-1].sar
latest_ema_results = ema_results[-1].ema
# print(latest_volatility_stop)
# latest_volatility_stop=float(latest_volatility_stop)
# Get the most recent closing price
latest_close_price = weekly_data['close'].iloc[-1]
lat_cl_p=float(latest_close_price)
# Determine if it's in "no sell zone" or "sell zone"
# if latest_volatility_stop > lat_cl_p:
#     print("Today's price is in the Sell Zone")
# else:
#     print("Today's price is in the No Sell Zone")

# dates = [quote.date for quote in quotes_list]
# prices = [quote.close for quote in quotes_list]
# vstop_values = [quote.sar for quote in vstop_results]
# sar_values = [quote.sar for quote in sar_results]

# Create a plot
# plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

# # # Plot the stock price
# plt.plot(dates, prices, label='Price', color='blue')

# # # Plot the SMA line
# plt.plot(dates, vstop_values, label='VStop', color='red')

# # # Add labels and title
# plt.xlabel('Date')
# plt.ylabel('Price / VSTOP')
# plt.title('Stock Price vs. VStop')

# # Add a legend
# plt.legend()

# # Show the plot
# plt.grid(True)
# plt.tight_layout()
# plt.show()
