from datetime import timedelta

import pandas as pd

# 讀檔
df = pd.read_csv(
    filepath_or_buffer='01 Order Rushing/order_brush_order.csv',
    parse_dates=['event_time']
)

# 排序比較好看，也可不用
df = df.sort_values(by=['event_time'])

# 結果，初始化
output = pd.DataFrame(data={'shopid': df['shopid'].unique(), 'userid': '0'})

# groupby shopid
for name, group in df.groupby('shopid'):
    # 迭代每一列
    for index, row in group.iterrows():

        # 每一列的一小時區間
        start = row['event_time']
        end = start + timedelta(hours=1)

        # 找出一小時區間有哪些資料
        one_hour_group = group.loc[
            (group['event_time'] >= start) &
            (group['event_time'] <= end)
        ]

        # Concentrate rate = Number of Orders within 1 hour / Number of Unique Buyers within 1 hour
        unique_buyers = one_hour_group['userid'].nunique()
        orders = one_hour_group['orderid'].count()
        concentrate_rate = orders / unique_buyers

        if concentrate_rate >= 3:
            output.loc[output['shopid'] == name, 'userid']
