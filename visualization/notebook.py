# %% Jupter Notebook - Data Visualization with HDF5 from Webscraping Data
# Import modules
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
import math

# %% Access data from HDF5 file located in hdf5 folder
# Python file location
script_dir = os.path.dirname(__file__)
file_name = 'data_collection.h5'
h5_path = os.path.join(script_dir, '../hdf5/') + file_name

# %% Open HDF5 file and create DataFrames
# h5_keys = [
#     'api_data', 'api_logs', 
#     'html_data', 'html_logs', 
#     'wss_data', 'wss_logs'
#     ]

df_api = pd.read_hdf(h5_path,key='api_data')
df_api_log = pd.read_hdf(h5_path,key='api_logs')

df_html = pd.read_hdf(h5_path,key='html_data')
df_html_log = pd.read_hdf(h5_path,key='html_logs')

df_wss = pd.read_hdf(h5_path,key='wss_data')
df_wss_log = pd.read_hdf(h5_path,key='wss_logs')

df_api['timestamp'] =  pd.to_datetime(df_api['timestamp'], format = '%Y-%m-%d')
# Used to show capture moments that are joined together (temporal developments)
df_api_log['start_dt'] =  pd.to_datetime(df_api_log['start_dt'], format = '%Y-%m-%d')

df_html['updated'] =  pd.to_datetime(df_html['updated'], format = '%Y-%m-%d')
df_html_log['timestamp'] = pd.to_datetime(df_html_log['timestamp'], format = '%Y-%m-%d')
# Add latitude and longitude columns
df_html['latitude'] = df_html['georss_point'].str.split(expand=True)[0].astype('float')
df_html['longitude'] = df_html['georss_point'].str.split(expand=True)[1].astype('float')

df_wss['timestamp'] =  pd.to_datetime(df_wss['timestamp'], format = '%Y-%m-%d')
df_wss_log['timestamp'] =  pd.to_datetime(df_wss_log['timestamp'], format = '%Y-%m-%d')

# %% Show general information about the API DataFrame
print(df_api.head())
df_api.info()
df_api.describe()

# %% Show api log information
print(df_api_log.head())
df_api_log.info()
df_api_log.describe()

# %% Plot API DataFrame for Temporal Development on close price
date_ranges_api = []
for i in range(len(df_api_log['start_dt'])):
    if(i<len(df_api_log['start_dt'])-1):
        date_ranges_api.append([
            df_api_log['start_dt'].iloc[i],
            df_api_log['start_dt'].iloc[i+1]
            ])
        # print(df_api_log['start_dt'].iloc[i],df_api_log['start_dt'].iloc[i+1])
    else:
        # print(df_api_log['start_dt'].iloc[i], 'Open ended')
        # The open-ended date (e.g. after last time data collection), does not 
        # need to be colored as we can put the whole price chart in distic color below
        # all the date_range_api overlays that sit on top.
        pass

# Create a sub-plot overlay for each date range
fig, ax = plt.subplots(figsize=(14,7))
main_trend = sns.lineplot(data=df_api,ax=ax,x='timestamp',y='close',linewidth=2, label='Closing Price Trend')
# data=df[(df['Date'] > '2018-11-30') & (df['Date'] < '2019-01-01')]
for _begin,_end in date_ranges_api:
    # Period Overlays
    overlay = sns.lineplot(
        data = df_api[
            (df_api['timestamp'] > _begin) & (df_api['timestamp'] < _end)
            ],
            ax=ax,
            x='timestamp',
            y='close',
            linewidth=2)
ax.vlines(
    x = df_api_log['start_dt'],
    ymin = 29000, 
    ymax= 30300,
    colors = ['#cdecee'],
    linestyles = ["dashed"],
    label = "Period")

# Legend and Info
plt.suptitle("BTC-USD Temporal Developments")
plt.title("Source: Coingecko API")
plt.legend()
plt.show()

# %% Show general information about the HTML DataFrame
print(df_html.head())
df_html.info()
df_html.describe()

# %% Show HTML log information
print(df_html_log.head())
df_html_log.info()
df_html_log.describe()

# %% Import Map Modules
# libraries
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt


# %% Plot HTML DataFrame for Temporal Development on earthquake data
date_ranges_html = []
for i in range(len(df_html_log['timestamp'])):
    if(i<len(df_html_log['timestamp'])-1):
        date_ranges_html.append(
            [
                df_html_log['timestamp'].iloc[i].tz_localize('UTC'),
                df_html_log['timestamp'].iloc[i+1].tz_localize('UTC')
            ])
        # print(df_html_log['timestamp'].iloc[i],df_html_log['timestamp'].iloc[i+1])
    else:
        # print(df_html_log['timestamp'].iloc[i], 'Open ended')
        # The open-ended date (e.g. after last time data collection), does not 
        # need to be colored as we can put the whole price chart in distic color below
        # all the date_ranges_html overlays that sit on top.
        pass

# %%
# Set the plot size for this notebook:
plt.figure(figsize=(10, 6.5))

#cyl
m=Basemap(llcrnrlon=-180, llcrnrlat=-60,urcrnrlon=180,urcrnrlat=80, projection='cyl' )
m.drawmapboundary(fill_color='#A6CAE0')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='white', alpha=0.2)

# Create Color Pallet based on number of different logging periods we have available
color_palette = sns.color_palette("viridis_r", n_colors=len(date_ranges_html))
# Convert to HEX colors
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
# Convert the color palette to hexadecimal color hashes
color_hashes = [rgb_to_hex((int(r * 255), int(g * 255), int(b * 255))) for r, g, b in color_palette]

for indx, val in enumerate(date_ranges_html):
    _begin, _end = val
    # Period Overlays
    period_x = df_html[(df_html['updated'] > _begin) & 
            (df_html['updated'] < _end)]

    period_y = df_html[(df_html['updated'] > _begin) & 
            (df_html['updated'] < _end)]
    
    m.scatter(
        latlon = True,
        x = period_x['longitude'],
        y = period_y['latitude'], 
        s = 100,
        c = color_hashes[indx], 
        marker = 'o', 
        alpha = 0.85, 
        edgecolor = 'k',
        linewidth = 1,
        zorder = 2,
    )

sc = m.scatter(
        latlon = True,
        x = 0,
        y = 0, 
        s = 0,
        c = 'red', 
        marker = 'o', 
        alpha = 0,
        linewidth = 1,
        zorder = 2,
    )

# Determine the starting date and end date for x-axis ticks
start_date = df_html['updated'].min()
end_date = df_html['updated'].max()

# Generate custom datetime ticks at a desired frequency
num_ticks = len(date_ranges_html)  # Number of desired ticks (including start and end dates)
timestamps = pd.date_range(start=start_date, end=end_date, periods=num_ticks).date
values = [mdates.date2num(pd.to_datetime(date)) for date in timestamps]

# Create the color bar
ax = plt.gca()
sm = plt.cm.ScalarMappable(cmap="viridis_r", norm=plt.Normalize(vmin=min(values), vmax=max(values)))
sm._A = []  # Dummy variable to trick matplotlib colorbar
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.05)
cbar.set_label('Dates', fontsize=12)

# Set the custom datetime ticks on the x-axis
cbar.ax.set_xticks(timestamps, rotation=90)
cbar.ax.set_xticklabels(timestamps, rotation=90, ha='left')

# Legend and Info
plt.suptitle("Earthquakes Temporal Developments")
plt.title("Source: earthquake.usgs.gov")
plt.tight_layout()
plt.show()

# %% Show general information about the HTML DataFrame
print(df_wss.head())
df_wss.info()
df_wss.describe()

# %% Show HTML log information
print(df_wss_log.head())
df_wss_log.info()
df_wss_log.describe()

# %% Plot WSS DataFrame for Temporal Development on earthquake data

# Since Websocket generates many timestamps entries in log we will specifically look for entries
# where connection was established instead of indivual trade messages

filter_on_open = df_wss_log[df_wss_log['update'] == 'ok']['timestamp']
# print(filter_on_open)

date_ranges_api = []
for i in range(len(filter_on_open)):
    if(i<len(filter_on_open)-1):
        date_ranges_api.append([
            filter_on_open.iloc[i].tz_localize('UTC'),
            filter_on_open.iloc[i+1].tz_localize('UTC')
            ])
    else:
        pass

# Create a sub-plot overlay for each date range
fig, ax = plt.subplots(figsize=(14,7))
main_trend = sns.lineplot(data=df_wss,ax=ax,x='timestamp',y='price',linewidth=2, label='XBTUSD Price Trend')
# data=df[(df['Date'] > '2018-11-30') & (df['Date'] < '2019-01-01')]
for _begin,_end in date_ranges_api:
    # Period Overlays
    overlay = sns.lineplot(
        data = df_wss[
            (df_wss['timestamp'] > _begin) & (df_wss['timestamp'] < _end)
            ],
            ax=ax,
            x='timestamp',
            y='price',
            linewidth=2)
ax.vlines(
    x = filter_on_open,
    ymin = 28985, 
    ymax= 30350,
    colors = ['#cdecee'],
    linestyles = ["dashed"],
    label = "Websocket Session")

# Legend and Info
plt.suptitle("XBT-USD Temporal Developments")
plt.title("Source: Bitmex Websocket")
plt.legend()
plt.show()

# %%
