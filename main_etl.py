import pandas as pd
import numpy as np
from datetime import datetime
import re
import os

from modules.file_check import validate_file
from modules.quality_check import data_quality_check

path = os.getcwd()
# path = path + '\inmar_py_2507'

print(f'Root path:\nPath: {path}')

current_year = 2021
current_month = 5
current_day = 27 # shouold only modify the day with 25, 27 or 28

short_year = str(current_year)[2:]  
if current_month < 10:
    short_month = '0' + str(current_month)
else:
    short_month = str(current_month)
    
if current_day < 10:
    short_day = '0' + str(current_day)
else:
    short_day = str(current_day)

filepath = path + f'/input_folder/{current_year}{short_month}{short_day}/'
processed_path = path + '/processed/'
unproc_path = path + '/unprocessed/'
raw_path = processed_path + 'raw/'

# Create the raw/<today> path if it doesn't exist    
if not os.path.exists(raw_path + f'{short_year}{short_month}{short_day}/'):
    os.makedirs(raw_path + f'{short_year}{short_month}{short_day}/')
    # print(f'Created dir: {raw_path} + {short_year}{short_month}{short_day}\')
    print(f'Created dir: {raw_path}{short_year}{short_month}{short_day}/')


write_path = raw_path + f'{short_year}{short_month}{short_day}/'

# Sends files that pass the check to processed/raw/<day>
# Sends files that fail the check to unprocessed
is_valid_file, data_df = validate_file(filepath, processed_path, unproc_path, write_path)

# We will work on with the input files at raw/<day>

data_quality_check(write_path, processed_path)

if __name__ == "__main__":
    print(f'\nDone processing files.\n.')
    print(f'\nDate', current_year, short_month, short_day, f'\nCWD: {path}\nFile path: {filepath}\nProcessed path: {processed_path}\nRaw: {raw_path}')

    # C:\Users\user\OneDrive\Inmar_intel\pcelaython_exercise\inmar_py_2507\input_folder\20210527