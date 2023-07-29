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
| --------- | ---- | ---- | --- | ----- |
| 2023-07-21 16:30:00 | 29861.85 | 29865.07 | 29829.82 | 29829.82 |
#### Log
For the log we save the start datetime, response datetime, error, status code and if it was successfull
| start_dt | response_dt | error | status_code | success |
| -------- | ----------- | ----- | ----------- | ------- |
| 2023-07-22 16:00:02.099107 | 2023-07-22 16:00:03.981783 | '' | 200 | True |

### HTML Format
#### Data

#### Log

### Websocket Stream Format
#### Data

#### Log


## After Data Collection
In the example we collected 5 days worth of data using automated cron tasks. No side effects or anomalies were detected in the log files which takes us to the next step of reading all csv files and combining them in a single HDF5 file. This can be done in the hdf5 folder using the following command and will output the file 'data_collection.h5' in the same directory:
`python3 data2hdf5.py`

# Example Data
Each scrape_ folder also contains a snippet of data of what we expect to receive and can be used to understand the structure of the data.

# Disclaimer
The developed application is licensed under the GNU General Public License.