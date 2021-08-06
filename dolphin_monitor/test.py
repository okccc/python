import datetime
import time

print(datetime.datetime.now().weekday())
current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print(current)
print(time.daylight)