# import csv
#
# import pandas as pd
#
# f = open('./text/write.csv', 'a', newline='', encoding="utf-8")
# wr = csv.writer(f)
# wr.writerow([1, '림코딩', '부산'])
# wr.writerow([2, '김갑환', '서울'])
#
# f.close()

from datetime import datetime
today = datetime.today()
year = today.year
month = today.month
day = today.day
hour = today.hour
minute = today.minute
current_time = str(year)[-2:] + str(month) + str(day) + str(hour) + str(minute)
print(current_time)