# IU INTERNATIONAL UNIVERSITY OF APPLIED SCIENCES
## General Course Context
Data storage capacities have increased with an exponential pattern in the last couple of years and decades. This has led to higher data availability. This, in turn, led to more and more data-driven and data-intensive analyses and applications for which, nowadays, our everyday lives are hard to imagine without them. The results of these analyses and applications can only be as good as the data with which the algorithms are fed. The reality today is that organizations that have data of high quality and know how to put these to use are way more successful than those that do not do so. This is the reason why we can consider data an organization's asset and one of its main assets actually. To increase data quality in an organization, we take several measures in the context of data quality management. But at the beginning of each data-related project, there is the question: How do I get the data I need? 

We will learn different techniques to obtain data that will be the basis for many of our analyses and processes. As working with data, basically, is sorting information into one shape or another, we will also enable ourselves to work with common data formats. Learning about these formats, their advantages, and disadvantages for a specific use case, and also their inner workings will allow us to access a real treasure of information that can improve the results of our applications or analyses. Finally, we will learn to tidy up our data. When we tidy our data, we bring it into a shape and structure that is easy to work with and straightforward to present in data visualizations. When done properly, this can reduce the time spent per project to prepare the data before answering a specific question or solving a particular problem. Also, equipped with the skills to tidy data, we can recognize patterns that might have gone unnoticed before.

## Webscraping Scripts for Data Quality and Data Wrangling (DLBDSDQDW01)
The following scripts use the following core modules like `requests`, `websocket`, `bs4` to obtain data in various ways. E.g. scraping html pages, authorized API access and utilizing websocket streams.

## Assignment
**1.2 Task 2: Scrape the Web**

You work for an organization which regularly consults several webpages to be informed in order to make key decisions. These web pages list numbers and tables which help decision makers in your organization to make informed decisions about strategic directions to be pursued. This process is conducted daily and manually and you start wondering if this might be better handled by an automated process. In addition, the question has been raised repeatedly within your organization if it is enough to only make decisions based on the most recent information or if it were better to also take a glimpse at the development of values over time.
In this task, you demonstrate your web scraping skills to collect information from several web pages, extract the relevant numeric information and save the results in a format which allows for time series considerations.

• Select at least three web pages of your choice which list numeric information daily. This could be plain numbers, tables, or something similar. Document your choice in a CSV file, so it will be easier to substitute these web pages later on. Make sure that scrapping these pages complies with the respective usage policies. You should discuss possible issues with respect to this as part of your assignment.
• Write a Python script which scraps the numeric information from the web pages as listed in the CSV file from the first step. Make your Python script executable on a daily basis. Demonstrate that you have acquired suitable skills during the course and compare your approach with other applied examples in the literature.
• Save the results into a HDF5 file. To make the data reusable for later analyses, you should reason for a suitable data model (e.g. how you decide in which shape to store the data).
• After your process has collected data over a couple of days, create a visualization which shows the temporal development of the respective values. Discuss the value added of your approach.
• Put yourself in a meta perspective and discuss and conclude your results in comparison to other studies and best practice examples from the literature.

## Purpose
The scripts provides users to scrape websites in a versatile manner and serve as examples as the structure of sites can differ. It only serves as Educational purposes in the context of the course DLBDSDQDW01 from IU.

Collected data comes in different formats and it's important to recognize the different types and structures it comes in. By utilizing various modules in Python the data is transformed in the desired format and written to a final HDF5 file which is frequently used in big data for storing large amount of information. As seen in the following image, which shows all csv's loaded into DataFrames:

![Alt text](csv2df.png?raw=true "Dataframes")

Tools like HDFView can be used to view the HDF5 file written by Pandas, which shows all our collected data in tables:

![Alt text](HDFView.png?raw=true "Dataframes")

Lastly, the data is investigated briefly using summary statistics and visualizations to ensure that it is error free, appropiate for further use (e.g. data analysis) and to make the temporal changes visible that are obtained by scraping the web. A final reflection is made to discuss and conclude the process that was used in context with other best practises and examples from the literature.

# Development Planning of the 3 webscrape techniques - UML Schemas
## Flow Diagram
![Alt text](UML.jpg?raw=true "UML Flow Diagram")

# How To Get Started
## Dependencies
Python 3.10+
## Installation Instruction
`git clone https://github.com/DeusNexus/data-wrangling.git`

`cd data-wrangling`

`pip3 install -r requirements.txt`

## Run The Application
You can manually run the files in each scraping folder or use cron (linux) to schedule a task. The API and HTML scraper only run once and finish automatically. The websocket connection keeps a live session for 4 hours while it collects all the trade data and writes it to CSV after completion. Find the files in the designated folders.

Example to run API:
`python3 scrape_api.py`

Example to run HTML:
`python3 scrape_html.py`

Example to run WSS:
`python3 scrape_wss.py`

## Using cron (example at 12:00PM and 00:00AM)
### Runs single process once
`0 12 * * * python3 /home/user/DataWrangling/Project/scrape_api/scrape_api.py`

`0 0 * * * python3 /home/user/DataWrangling/Project/scrape_api/scrape_api.py`

### Runs a stream that terminates after 4 hours
`0 12 * * * python3 /home/user/DataWrangling/Project/scrape_wss/scrape_wss.py`

`0 0 * * * python3 /home/user/DataWrangling/Project/scrape_wss/scrape_wss.py`

### Runs single process once
`0 12 * * * python3 /home/user/DataWrangling/Project/scrape_html/scrape_html.py`

`0 0 * * * python3 /home/user/DataWrangling/Project/scrape_html/scrape_html.py`

## Data Collection
The processes will each output 2 files (or 1 in case of error in the logs) which are stored in the data and logs folder respectively. The logs will contain information about successfull responses and errors that have occured.
`data_<process specific>_<iso-datetime>.csv` or `logs_<process specific>_<iso-datetime>.csv`

### API Format
API requests are made using `requests` library and returned in `json` format.  
#### Data
The data is mostly kept as it is with the following columns (example):
| timestamp | open | high | low | close |
| --------- | --------- | --------- | --------- | --------- |
| 2023-07-21 16:30:00 | 29861.85 | 29865.07 | 29829.82 | 29829.82 |
#### Log
For the log we save the start datetime, response datetime, error, status code and if it was successfull
| start_dt | response_dt | error | status_code | success |
| --------- | --------- | --------- | --------- | --------- |
| 2023-07-22 16:00:02.099107 | 2023-07-22 16:00:03.981783 | '' | 200 | True |

### HTML Format
#### Data
From the HTML structure a lot of data has been extracted, some of which is enriched using diagram from their official page (e.g. the magnitude shaking, magnitude damage).
In the script file regex is also used to match certain strings to extract kilometers and miles respecificly or number of reports.
| id | title | updated | link_href | num_of_reports | time_utc | time_utc_at_epicenter | location_coordinates | depth_string | depth_km | depth_mi | georss_point | georss_elev | cat_age |cat_mag | cat_mag_shaking | cat_mag_damage | cat_contributor | cat_author |
| --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- |--------- | --------- | --------- | --------- | --------- |
| urn:earthquake-usgs-gov:us:7000khmu | M 4.7 - South Sandwich Islands region | 2023-07-22T15:51:37.040Z | https://earthquake.usgs.gov/earthquakes/eventpage/us7000khmu | 5 | 2023-07-22 15:03:30 UTC | 2023-07-22 15:03:30 UTC | 57.942°S 25.376°W | 56.33 km (35.00 mi) | 56.33 | 35.00 | -57.9422 -25.3756 | -56326 | Past Hour | Magnitude 4 | Light | None | us | us |

#### Log
The log is simpler, any error catched while parsing the HTML structure is saved so one can look back later what went wrong including the data which is saved under the data column.
This time also calculation is performed how long the request took in ms to complete, optional attributes like this can be included if desired.
| timestamp | url | err_msg | err_obj | data | req_status | method | execution_time_ms |
| --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- |
| 2023-07-23T00:00:03.369724 | https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.atom | OK | None | "<?xml version='1.0' encoding='UTF-8'?><html><body><feed xmlns='http://www.w3.org/2005/Atom' xmlns:georss='http://www.georss.org/georss'>...</feed></body></html>" | 200 | request-beatifulsoup | 20.889997482299805 |


### Websocket Stream Format
The websocket stream yields the highest velocity of data as it arrives in real-time and in a continuous manner. For a period of 4 hours a large amount of messages is received and stored which for the 5 day window yielded over 30,000 unique entries! The processing, storage and utilization have to be determined based on the goal in mind.
#### Data
The following attributes as received are stored which could be interesting for various analysis.
| timestamp | symbol | side | size | price | tickDirection | trdMatchID | grossValue | homeNotional | foreignNotional | trdType |
| --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- |
| 2023-07-28T16:00:01.745Z | XBTUSD | Buy | 4000 | 29375.5 | ZeroPlusTick | e1bd7555-4df1-0f28-36aa-5c0e263755ba | 13616800 | 0.136168 | 4000.0 | Regular |

#### Log
Due to the high velocity and constant data stream it is important to have quick and specific error messages / logging available. Real-time environments operate at fast pace and if a service goes down or large part of data is missing it can be bad for the business. The webstream pings the server at fixed interval to check if the connection is still alive, which is also seen in the log. Sometime it does occur that internet connection drops and it needs to re-establish the connection which are recorded. 

Errors that arise have information about the function that occured in, state of the message (OPEN/SUBSCRIBE/INFO/ACTION/HEARTBEAT). 

The ACTION message arrive in 2 forms (partial & insert); partial is a snapshot of for example the most recent orderbook or trades that already occured, inserts are real-time updates happening after/during the connection is established.
| timestamp | last_update | init | num_updates | num_errors | total_pong | total_timeout | total_reconnect | func_name | state | update | message |
| --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- |
| 2023-07-22T16:00:03.764 | 2023-07-22 16:00:03.743766 | True | 0 | 0 | 0 | 0 | 0 | on_open | OPEN | ok | Connection opened on websocket! |
| 2023-07-22T16:00:03.785 | 2023-07-22 16:00:03.743766 | True | 0 | 0 | 0 | 0 | 0 | on_open | SUBSCRIBE | send | "{'op': 'subscribe', 'args': ['trade:XBTUSD']}" |
| 2023-07-22T16:00:03.816 | 2023-07-22 16:00:03.743766 | False | 0 | 0 | 0 | 0 | 0 | on_message | INFO | | "{'remaining': 179},{'info': 'Welcome to the BitMEX Realtime API.', 'version': '2.0.0', 'timestamp': '2023-07-22T16:00:03.554Z', 'docs': 'https://www.bitmex.com/app/wsAPI', 'heartbeatEnabled': False, 'limit': {'remaining': 179}}" |
| 2023-07-22T16:00:04.311 | 2023-07-22 16:00:03.743766 | False | 0 | 0 | 0 | 0 | 0 | on_message | SUBSCRIBE | true | trade:XBTUSD |
| 2023-07-22T16:00:04.326 | 2023-07-22 16:00:03.743766 | False | 1 | 0 | 0 | 0 | 0 | on_message | ACTION | partial |
| 2023-07-22T16:00:05.841 | 2023-07-22 16:00:03.743766 | False | 2 | 0 | 0 | 0 | 0 | on_message | ACTION | insert |
| 2023-07-22T16:00:06.152 | 2023-07-22 16:00:03.743766 | False | 3 | 0 | 0 | 0 | 0 | on_message | ACTION | insert |

## After Data Collection
In the example we collected 5 days worth of data using automated cron tasks. No side effects or anomalies were detected in the log files which takes us to the next step of reading all csv files and combining them in a single HDF5 file. This can be done in the hdf5 folder using the following command and will output the file 'data_collection.h5' in the same directory:
`python3 data2hdf5.py`

## Visualization of Temporal Developments
The main focus is on the collected `data` albeit it's also great to explore the `logs` for any potential insights regarding errors, optimization and general understanding of how the data collection process materialized. For each of the different scrape methods visualization have been created which allow us to reflect on the characteristics of the data obtained. Data scraped twice a day, some of the data has overlapping entries since the newly added information might contain data that was already present in an early scrape. Loaded from HDF5 to Pandas DataFrame, duplicates have been removed at the stage when the HDF5 file was created. 

### API Plot
Since we are interested in the temporal developments the `timestamp` column is used on x-axis as datetime format.
There serveral features to chose from but for simplicty the `close` source was used to show the price developments. To emphasize the added value of scraping multiple times each obtained window is displayed in it's own color. We are now able to take a larger scope of price developments in consideration which enhances our understanding, decision making and improves statistical confidence. Here each new batch is made visible by using vertical lines that show how new data is added.

![Alt text](./visualization/API_visual.png?raw=true "API Visualisation")

### HTML Plot
Here for temporal developments the `updated` column is used. 
From all the features the location coordinates and the dates are what is most important about the collected data. In this map plot we can see how new earthquakes were added based on the changing color which is depicted in the dates below. Without the daily scraping many observations would be left out and with further analyis lead to a lack of data if one is trying to predict new earthquake events.

![Alt text](./visualization/HTML_visual.png?raw=true "HTML Visualisation")

### Websocket Plot
The `timestamp` column is used on x-axis similar to the API plot. A major difference with the websocket is that the connection is continuous and sometimes drops.
Each session that the websocket is connected is indicated by vertical lines. Furthermore, after the high velocity of data is done (4 hours) the data does not have any new values and shows 'no trend' until new session starts.
What makes websocket streams powerful is the amount of data received in real-time and the missing values between sessions indicate that these also require additional awareness on how to deal with missing values or maintaining a good connection in general.

![Alt text](./visualization/WSS_visual.png?raw=true "WSS Visualisation")

# Example Data
Each scrape_ folder also contains a snippet of data of what we expect to receive and can be used to understand the structure of the data.

# Disclaimer
The developed application is licensed under the GNU General Public License.