import pandas as pd
import numpy as np

# Load your data here (replace 'file.json' with the path to your dataset)
data = pd.read_json('file.json')

data['t'] = pd.to_datetime(data['t'], unit='ms')  # Convert timestamp to datetime

# Bollinger Bands Parameters
band_width_threshold = 0.006  # Define threshold for sideways market detection
atr_threshold = 20  # ATR threshold for low volatility
adx_threshold = 20  # ADX threshold for weak trend
rsi_lower, rsi_upper = 40, 60  # RSI thresholds for sideways markets

# Calculate Bollinger Bands
def calculate_bollinger_bands(df, period=20, std_dev=2):
    df['Middle Band'] = df['c'].rolling(window=period).mean()
    df['Std Dev'] = df['c'].rolling(window=period).std()
    df['Upper Band'] = df['Middle Band'] + (std_dev * df['Std Dev'])
    df['Lower Band'] = df['Middle Band'] - (std_dev * df['Std Dev'])
    df['Band Width'] = (df['Upper Band'] - df['Lower Band']) / df['Middle Band']
    return df

# Calculate ATR (Average True Range)
def calculate_atr(df, period=14):
    df['TR'] = np.maximum(df['h'] - df['l'], np.maximum(abs(df['h'] - df['c'].shift(1)), abs(df['l'] - df['c'].shift(1))))
    df['ATR'] = df['TR'].rolling(window=period).mean()
    return df

# Calculate ADX (Average Directional Index)
def calculate_adx(df, period=14):
    df['+DM'] = np.where((df['h'] - df['h'].shift(1)) > (df['l'].shift(1) - df['l']), 
                         np.maximum(df['h'] - df['h'].shift(1), 0), 0)
    df['-DM'] = np.where((df['l'].shift(1) - df['l']) > (df['h'] - df['h'].shift(1)), 
                         np.maximum(df['l'].shift(1) - df['l'], 0), 0)
    df['TR'] = np.maximum(df['h'] - df['l'], np.maximum(abs(df['h'] - df['c'].shift(1)), abs(df['l'] - df['c'].shift(1))))
    df['+DI'] = 100 * (df['+DM'].rolling(window=period).sum() / df['TR'].rolling(window=period).sum())
    df['-DI'] = 100 * (df['-DM'].rolling(window=period).sum() / df['TR'].rolling(window=period).sum())
    df['DX'] = 100 * abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI'])
    df['ADX'] = df['DX'].rolling(window=period).mean()
    return df

# Calculate RSI (Relative Strength Index)
def calculate_rsi(df, period=14):
    delta = df['c'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# Apply calculations
data = calculate_bollinger_bands(data)
data = calculate_atr(data)
data = calculate_adx(data)
data = calculate_rsi(data)

# Identify sideways market conditions
data['Sideways'] = (
    (data['Band Width'] < band_width_threshold) &
    (data['ATR'] < atr_threshold) &
    (data['ADX'] < adx_threshold) &
    (data['RSI'] > rsi_lower) &
    (data['RSI'] < rsi_upper)
)

# Identify points of maximum compression
data['Max Compression'] = data['Sideways'] & (data['Band Width'] == data['Band Width'].rolling(window=5).min())

# Initialize positions list
positions = []
current_position = None

# Strategy logic
for i in range(len(data)):
    row = data.iloc[i]

    if row['Max Compression']:
        if row['c'] > row['Upper Band']:  # Impulse up
            if current_position != "LONG":
                if current_position == "SHORT":
                    positions[-1]['exit_price'] = row['c']
                current_position = "LONG"
                positions.append({'entry_time': row['t'], 'entry_price': row['c'], 'type': 'LONG'})
        elif row['c'] < row['Lower Band']:  # Impulse down
            if current_position != "SHORT":
                if current_position == "LONG":
                    positions[-1]['exit_price'] = row['c']
                current_position = "SHORT"
                positions.append({'entry_time': row['t'], 'entry_price': row['c'], 'type': 'SHORT'})

    if row['Sideways'] and current_position:
        positions[-1]['exit_time'] = row['t']
        positions[-1]['exit_price'] = row['c']
        current_position = None

# Convert positions to DataFrame
trades = pd.DataFrame(positions)
trades['profit'] = trades['exit_price'] - trades['entry_price']
trades.loc[trades['type'] == 'SHORT', 'profit'] *= -1

# Print trade summary
print(trades)
print("\nTrade Summary")
print("Total Trades:", len(trades))
print("Winning Trades:", len(trades[trades['profit'] > 0]))
print("Losing Trades:", len(trades[trades['profit'] <= 0]))
print("Total Profit:", trades['profit'].sum())
print("Average Profit per Trade:", trades['profit'].mean())
