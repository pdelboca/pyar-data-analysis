# io.py: Loads data from csv/database into python session
# (Highly recommend pandas DataFrame).
#
# Your I/O file should be responsible for loading any data required for your
# project. Perform any merging, munging, or any other data cleansing tasks so
# that your data is nice and neat and ready to be trained.

import pandas as pd
import os
import mailbox

path = os.path.dirname(os.path.abspath(__file__))

def get_dataframe(self):
    csv_path = path + '/data/pyar.csv'
    df = pd.read_csv(csv_path)
    return df