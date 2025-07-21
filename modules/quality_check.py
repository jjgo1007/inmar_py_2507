import pandas as pd
import numpy as np
import os
import re

def final_phone(raw_phone):
    # Handle nulls and identified not reported data, list might grow later
    if pd.isna(raw_phone) or str(raw_phone).strip().lower() in ('na', ''):
        return []
    # Split string of phones but new line separator
    phones = re.split(r'[\r\n]+', str(raw_phone).strip())
    
    # cleanse elements of the list to remove any non-numeric character
    clean_list = [re.sub(r'[^\d]', '', p) for p in phones if p.strip()]
    return clean_list

def valid_phone_list(phone_list):
    # Validate a list of phone numbers against Indian formats
    # found two general validations, might be improved or applied to different coutry formats
    
    landline_pat = r'^0[2-9]\d{5,9}$'     # Landline: 0 + 2-9 + 5-9 digits
    mobile_pat = r'^(?:91)?[6-9]\d{9,10}$' # Mobile: 91 + 6-9 + 9 or 10 digits (91 is optional)
                
    phone_str = str(phone_list)
    
    return bool(
        re.fullmatch(landline_pat, phone_str) or
        re.fullmatch(mobile_pat, phone_str)

    )

def data_quality_check(write_path, processed_path):
    columns = ['url','address','name','online_order','book_table','rate', 'votes','phone','location','rest_type','dish_liked','cuisines',
                                             'approx_cost(for two people)','reviews_list','menu_item', 'listed_in(type)','listed_in(city)']
    
    files = [entry.name for entry in os.scandir(write_path) if entry.is_file()] # list of files in the path
    for filename in files:
        pattern = r'[^0-9A-Za-z ()[\]\'.,":;\\/-]' # some special characters that should be keeped to don't mess with the coumns and sentences
        df = pd.read_csv(write_path + filename)

        df['row_number'] = range(1, len(df)+1)
        df['valid_phones'] = df['phone'].apply(final_phone).apply(lambda ls: list(filter(valid_phone_list, ls)))
        df['phone_good'] = df['valid_phones'].apply(lambda ls: 1 if len(ls) >= 1 else 0)
        df['reported_name'] = df['name'].apply(lambda n: 0 if pd.isna(n) else 1)
        df['reported_location'] = df['location'].apply(lambda n: 0 if pd.isna(n) else 1)
        df['null_field'] = np.where((df['phone_good'] == 0)|(df['reported_name'] == 0)|(df['reported_location'] == 0), 1, 0)
        df['address'] = df['address'].astype(str).apply(lambda x: re.sub(pattern, '', x))
        df['reviews_list'] = df['reviews_list'].astype(str).apply(lambda x: re.sub(pattern, '', x))
        df['phone'] = df['valid_phones']

        # Fill bad_metadata.txt with file_name, reason, row_list
        bad_list_null = df.query('null_field == 1')['row_number'].tolist()

        with open(processed_path + 'bad_metadata.txt', 'a') as f:  
           f.write(f'{filename}|null|{bad_list_null}\n')
        
        print(f'Wrote records in {filename} in badmetadata.txt')

        # Split modified df in .out and .bad
        df_bad = df[df['null_field'] == 1]
        df_out = df[~df['row_number'].isin(df_bad['row_number'])]

        df_bad = df_bad[columns]
        df_out = df_out[columns]
        
        df_bad.to_csv(processed_path + filename + '.bad')
        print(f'Wrote records in {filename} in .bad file')

        df_out.to_csv(processed_path + filename + '.out')
        print(f'Wrote records in {filename} in .out file')

    return None
