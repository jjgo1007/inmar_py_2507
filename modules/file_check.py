import pandas as pd
# from datetime import datetime
import os

def validate_file(filepath, processed_path, unproc_path, write_path):
    # Read processed files
    processed_file_path = os.path.join(processed_path, 'processed_files.txt')
    process_df = pd.DataFrame(columns = ['url','address','name','online_order','book_table','rate',
                                         'votes','phone','location','rest_type','dish_liked','cuisines',
                                         'approx_cost(for two people)','reviews_list','menu_item',
                                         'listed_in(type)','listed_in(city)'])
    
    with open(processed_path + 'processed_files.txt', 'r') as f:
        processed_files = set(line.strip() for line in f.readlines())
    files = [entry.name for entry in os.scandir(filepath) if entry.is_file()] # list of files in the path
    files_to_add = []
    any_success = False
    
    for filename in files:
        
        if not filename.endswith('.csv'):
            print(f'Skip non csv file: {filename}')
            with open(unproc_path + 'unprocessed_log.txt', 'a') as f:  
                f.write(f'{filename}|non_csv\n')
            continue

        if os.path.getsize(filepath + filename) == 0:
            print(f'Skiping empty file: {filename}')
            with open(unproc_path + 'unprocessed_log.txt', 'a') as f:  
                f.write(f'{filename}|empty_file\n')
            continue

        if filename in processed_files:
            print(f'Skip already processed {filename}')
            with open(unproc_path + 'unprocessed_log.txt', 'a') as f:  
                f.write(f'{filename}|already_processed\n') 
            continue
        else:
            files_to_add.append(filename)
            # print(f'Added {filename} to log.\n{processed_path}processed_files.txt\nFiles_to_add: {files_to_add}')   
        
        try:
            df = pd.read_csv(filepath + filename)
            files_to_add = []
            print(f'{filename} Read Succesfull and copied to /processed/raw/')
            df.to_csv(write_path + filename)
            process_df = pd.concat([process_df, df], ignore_index = True)
            files_to_add.append(filename)
            any_success = True
            if files_to_add:
                with open(processed_file_path, 'a') as f:  
                    f.write('\n'.join(files_to_add) + '\n')
            #return True, df
        except Exception as e:
            print(f"exception reading file: {e}")
            # return False, None
            
    return any_success, process_df
