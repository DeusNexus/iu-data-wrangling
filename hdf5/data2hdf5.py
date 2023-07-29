import os
import pandas as pd
from model import model

# Declare root directory
root_dir = '/home/fox/Desktop/Project'

# Declare data dirs
data_scrape_dir = root_dir + '/scrape_api/data/'
data_html_dir = root_dir + '/scrape_html/data/'
data_wss_dir = root_dir + '/scrape_wss/data/'

# Declare log dirs
logs_scrape_dir = root_dir + '/scrape_api/logs/'
logs_html_dir = root_dir + '/scrape_html/logs/'
logs_wss_dir = root_dir + '/scrape_wss/logs/'

# Init dict for holding unique file names and paths
file_tree = {
    'api_data': [],
    'api_logs': [],
    'html_data': [],
    'html_logs': [],
    'wss_data': [],
    'wss_logs': [],
}

# Populate the file tree
for i in [data_scrape_dir,data_html_dir,data_wss_dir,logs_scrape_dir,logs_html_dir,logs_wss_dir]:
    for file_path in os.listdir(i):
        # Full file path
        full_path = i+file_path
        dict_key = ''

        if 'api/data/' in full_path:
            dict_key = 'api_data'
        elif 'api/logs/' in full_path:
            dict_key = 'api_logs'
        elif 'html/data/' in full_path:
            dict_key = 'html_data'
        elif 'html/logs/' in full_path:
            dict_key = 'html_logs'
        elif 'wss/data/' in full_path:
            dict_key = 'wss_data'
        elif 'wss/logs/' in full_path:
            dict_key = 'wss_logs'

        file_tree[dict_key].append(full_path)

# print(file_tree)

# Read every CSV in a folder and add to its own DataFrame. We keep the same name convention here so it is easier to link the DataFrame with their names as the keys in the file_tree
# The keys will be used as name for the HDF5 dataset names.
dfs_concat = {
    'api_data': {},
    'api_logs': {},
    'html_data': {},
    'html_logs': {},
    'wss_data': {},
    'wss_logs': {},
}
for key in file_tree.keys():
    indivual_dfs = []
    for fp in file_tree[key]:
        # Use comma seperator and when it is within a double quote ignore it!
        indivual_dfs.append(pd.read_csv(
            filepath_or_buffer=fp,sep=',',
            quotechar='"',
            skipinitialspace=True))
    # Now join each seperate csv DataFrame to get a single main DataFrame for each key in filetree
    df_concat = pd.concat(indivual_dfs)

    print(f'\n######## {key} ########\n',df_concat)
    # Set the correct dtypes and datecolumns using the model
    df_concat.astype(dtype=model[key]['cols'])
    df_concat.set_index(model[key]['index'],inplace=True)
    df_concat.sort_index(inplace=True)
    # Remove duplicated values that can occur e.g. when timeout happens and api reconnects or if scraping multilpe times in a day and the returned values overlap.
    df_concat = df_concat[~df_concat.index.duplicated(keep='first')]
    df_concat.reset_index(inplace=True)

    # Set the dict to the new concatenated DataFrame
    dfs_concat[key] = df_concat

    # Use for debugging
    # print(f'\n######## {key} ########',dfs_concat[key])

    # Finally now that each file is in a dataframe we can write it to HDF5
    # Note: we are still dealing with a relatively small dataset but if the amount of csv files grows large we would want to use a per-line approach so we don't overload the memory
    # The current files are around 15mb, large datasets with several GBs of data can quickly cause out of memory issues. Important to be aware of, but due to scope not added.

# After data has been loaded and correct dtype, datetime columns have been set it can be written to the HDF5 file
# with h5py.File('data_collection.h5', 'w') as hf:
#     for key in dfs_concat.keys():
#         df = dfs_concat[key]
#         # Use key as name for dataset and dataframe as data
#         # hf.create_dataset(key, data=df)
#         df.to_hdf('data_collection.h5','df',mode='w',format='table',data_columns=True)

for key in dfs_concat.keys():
    df = dfs_concat[key]
    # Use key as name for dataset and dataframe as data
    df.to_hdf('data_collection.h5',key=key,mode='a',format='table',data_columns=True)

