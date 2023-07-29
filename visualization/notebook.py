# %% Jupter Notebook - Data Visualization with HDF5 from Webscraping Data
# Import modules
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

# %% Access data from HDF5 file located in hdf5 folder
# Python file location
script_dir = os.path.dirname(__file__)
file_name = 'data_collection.h5'
h5_path = os.path.join(script_dir, '../hdf5/') + file_name

# %% Open HDF5 file
# file_keys = [
#     'api_data', 'api_logs', 
#     'html_data', 'html_logs', 
#     'wss_data', 'wss_logs'
#     ]

df_api = pd.read_hdf(h5_path,key='api_data')
df_html = pd.read_hdf(h5_path,key='html_data')
df_wss = pd.read_hdf(h5_path,key='wss_data')

df_api['timestamp'] =  pd.to_datetime(df_api['timestamp'], format = '%Y-%m-%d')
df_html['updated'] =  pd.to_datetime(df_html['updated'], format = '%Y-%m-%d')
df_wss['timestamp'] =  pd.to_datetime(df_wss['timestamp'], format = '%Y-%m-%d')


# %%
df_wss.head()
df_wss.info()
df_wss.describe()

# %%
# fig, ax = plt.subplots(figsize=(14,7))
# sns.lineplot(df_wss,ax=ax,x='timestamp',y='price')
sns.pairplot(df_html)
plt.show()

# %%

# %%
