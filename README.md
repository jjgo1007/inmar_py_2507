# inmar_py_2507
Repo to upload the Python exercise files

The ETl considers the /inmar_py_2507 as the starting path for all the processes, so the path must be set as follows, depending on the location it's downloaded to: 
    root_path # Where this repo is located
Set:
    path = root_path + '\inmar_py_2507'

All the log_files will start empty:
- path/processed/processed_files.txt
- path/processed/bad_metadata.txt
- path/unprocessed/unprocessed_log.txt
- path/processed/raw/<day> # folder with passed file check

The input files are located in the following folder, split into sub_folders by day (some dummy files to reject were added here):
- path/input_folder/20210525/
- path/input_folder/20210527/
- path/input_folder/20210528/
- There were a couple of dummy files created to check rejection for various reasons, and the successful execution of more than 1 file each day

The ETL to be executed is:
- path/main_etl.py
- Example of the terminal: PS C:\Users\user\OneDrive\Inmar_intel\python_exercise\inmar_py_2507> py main_etl.py

The 'current_day' variable should be modified with (25, 27, 28) to run the 3 days available in this demo. It only simulates the execution of one day at a time, but it does the entire process.

The quality check created a new phone output column, which contains a list of only the validated phone numbers, with the special characters removed. These will be in the .out file in the same place that the original 'phone' column was.

The general workflow is (for each day [25, 27, 28])
1. main_etl.py runs
2. Creates the folder to save all the files to process that day if it doesn't exist
3. It calls the file_check.py function; this checks the general requirements of the files, if they comply, it sends them to the processed/raw/<day> folder, if not, it sends them to the unprocessed folder and fills the unprocessed_log.txt with the reason it couldn't be processed
4. It calls the quality_check.py functions, which contain the phone validation, formatting, and output, the null check for the mandatory columns (name, phone, location), reads each file of the day, splits them into the .out and .bad files, and fills the bas_metadata.txt file.
