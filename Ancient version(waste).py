from datetime import datetime
import time

while True:
    now = datetime.now()
    print(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], flush=True)
    time.sleep(0.1)