# from datetime import date,timedelta
# from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save
# from jugaad_data.nse import stock_df

# def calculate_ema(df, column_name, window):
#     # ema = df[column_name].ewm(span=window, adjust=False).mean()
#     # return ema
#     ema = df[column_name].ewm(span=window, adjust=False).mean()
#     return ema.iloc[-1]

# df = stock_df(symbol="SBIN", from_date=date.today() - timedelta(days=20),
#             to_date=date.today(), series="EQ")

# ema_window = 10
# ema_20 = calculate_ema(df, 'CLOSE', ema_window)
# print(f'EMA_20: {ema_20}')
#   # You can adjust this to your desired EMA window
# # df['EMA'] = calculate_ema(df, 'CLOSE', ema_window)
# # print(df)
# # # DST9FVJ75B5VTSNK
# from datetime import date, timedelta
# from jugaad_data.nse import stock_df
# import matplotlib.pyplot as plt

# def calculate_ema(df, column_name, window):
#     if len(df) >= window:  # Check if there are enough data points to calculate EMA
#         ema = df[column_name].ewm(span=window, adjust=False).mean()
#         return ema
#     else:
#         return None

# df = stock_df(symbol="SBIN", from_date=date.today() - timedelta(days=20),
#               to_date=date.today(), series="EQ")

# ema_window = 10
# df['EMA'] = calculate_ema(df, 'CLOSE', ema_window)
# print(df)
# # Plotting the data
# plt.figure(figsize=(12, 6))
# plt.plot(df['DATE'], df['CLOSE'], label='Close Price', color='blue')
# plt.plot(df['DATE'], df['EMA'], label=f'EMA {ema_window}', color='orange')
# plt.title('Stock Price with EMA')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.legend()
# plt.grid(True)
# plt.show()
from datetime import date, timedelta
from jugaad_data.nse import stock_df
import matplotlib.pyplot as plt

def calculate_ema(df, column_name, window):
    ema_series = df[column_name].ewm(span=window, adjust=False).mean()
    return ema_series


df = stock_df(symbol="DELTACORP", from_date=date.today() - timedelta(days=30*7),
              to_date=date.today(), series="EQ")
print(date.today())
ema_window = 100
df = df.iloc[::-1]
# df.set_index('DATE', inplace=True)
# df_weekly = df.resample('W').mean()
filtered_df = df  # Filter rows with enough data points for EMA
print(filtered_df)
ema_series = calculate_ema(filtered_df, 'CLOSE', ema_window)

if not ema_series.empty:
    current_ema = ema_series.iloc[-1]
    previous_ema = ema_series.iloc[-2] if len(ema_series) >= 2 else ema_series.iloc[-1]
    current_price = df['CLOSE'].iloc[-1]

    if current_ema > current_price:
        print("Red Alert!")
    else:
        print("DeltaCorp" + "'s LTP is well above it's 20 weekly EMA")

# Plotting the data
# plt.figure(figsize=(12, 6))
# plt.plot(filtered_df['DATE'], filtered_df['CLOSE'], label='Close Price', color='blue')

# if not ema_series.empty:
#     plt.plot(filtered_df['DATE'], ema_series, label=f'EMA {ema_window}', color='orange')

# plt.title('Stock Price with EMA')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.legend()
# plt.grid(True)
# plt.show()
