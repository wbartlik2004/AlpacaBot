from talipp.indicators import SMMA, ZLEMA, SMA
import yfinance as yf
from datetime import datetime, timedelta

length_MA = 34
length_Signal = 9

symbol = 'AAPL'
end_date = datetime.now().date()
start_date = end_date - timedelta(days=180)
data = yf.download(symbol, start=start_date, end=end_date, interval='1D')
data['hlc3'] = (data['High'] + data['Low'] + data['Close']) / 3

hi = SMMA(period=length_MA, input_values=data['High'].tolist())
lo = SMMA(period=length_MA, input_values=data['Low'].tolist())
mi = ZLEMA(period=length_MA, input_values=data['hlc3'].tolist())

real_index = 0


for i in range(len(hi)-1):
    if hi[i + 1] is not None:
        real_index = i + 1
        break
print("index of hi:", real_index)

for i in range(len(lo)-1):
    if lo[i + 1] is not None:
        if real_index < i + 1:
            real_index = i + 1
            break
print("index of lo:", real_index)

for i in range(len(mi)-1):
    if mi[i + 1] is not None:
        if real_index < i + 1:
            real_index = i + 1
            break
print("index of mi:", real_index)

md = []

for i in range(len(mi)-real_index):
    if mi[real_index+i] > hi[real_index+i]:
        md.append(mi[real_index+i] - hi[real_index+i])
    elif mi[real_index+i] < lo[real_index+i]:
        md.append(mi[real_index+i] - lo[real_index+i])
    else:
        md.append(0)

sb = SMA(period=length_Signal, input_values=md)

sh = []
for i in range(len(md)-length_Signal):
    sh.append(md[i+length_Signal] - sb[i+length_Signal])
print(len(sh))

print("Last 5 values of md rounded to two decimal places:", [round(value, 2) for value in md[-5:]])
print("Last 5 values of sb rounded to two decimal places:", [round(value, 2) for value in sb[-5:]])
print("Last 5 values of sh rounded to two decimal places:", [round(value, 2) for value in sh[-5:]])
