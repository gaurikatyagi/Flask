import os

def find_csv_filenames( suffix= ".csv" ):
    path_to_dir = os.path.dirname(os.path.abspath(__file__))
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

if __name__ == "__main__":
    # print directory_path
    csv_files = find_csv_filenames()
