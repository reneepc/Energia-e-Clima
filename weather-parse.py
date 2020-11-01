import pandas as pd
import sys
import datetime

df = pd.read_csv(sys.argv[1])
for ts in df.time:
    print(datetime.datetime.fromtimestamp(ts).date())
