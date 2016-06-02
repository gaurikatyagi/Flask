import pandas

import os

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

if __name__ == "__main__":
    directory_path = os.path.dirname(os.path.abspath(__file__))
    # print directory_path
    print find_csv_filenames(directory_path)