from os.path import isfile, join
from os import listdir
import pandas as pd
from utils import get_files_paths_wich_contains

paths_directory = [
    './0',
    './5'
]

main_file_name_path = './main_class_five_&_zero.csv'
def get_files_paths_wich_contains(directory_path:str,s:str):
    return [f'{directory_path}/{f}' for f in listdir(directory_path) if isfile(join(directory_path, f)) if s in f]

def run(paths):
    dfs = []
    for path in paths:
        df = pd.read_csv(path)
        path_content = path.split('/')
        file_name = path_content[-1]
        event = path_content[-2]
        df['file_name'] = file_name
        df['event'] = event
        dfs.append(df)
    main_df = pd.concat(dfs)
    main_df.to_csv(main_file_name_path)
    return

def get_paths():
    master_well_paths:list = []
    for path in paths_directory:
        paths_files_directory = get_files_paths_wich_contains(path,'WELL')
        master_well_paths.extend(paths_files_directory)
    return master_well_paths

def merge_csvs_into_df(csvs_path_list:str):
    return pd.concat(map(pd.read_csv, csvs_path_list), ignore_index=True) if csvs_path_list else []

if __name__ == "__main__":
    paths = get_paths()
    run(paths)

    




