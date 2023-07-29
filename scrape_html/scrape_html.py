# load packages
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup as bs
import warnings
import re
import pandas as pd
import numpy as np

url='https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.atom'

#Supress Warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

model_output = {}

def main():
    try: # Start error catching here to see if we are referencing any tags that are not present while being called/searched for or when requesting url
        global model_output

        # load a web page
        page = requests.get(url)

        model_output = {
            'timestamp': datetime.now().isoformat(),
            'url':page.url,
            'err_msg': '',
            'err_obj': '',
            'data': '',
            'req_status': -1,
            'method': 'request-beatifulsoup',
            'execution_time_ms': 0
        }

        if page.status_code != '200':
            model_output['req_status'] = page.status_code
            model_output['err_msg'] = page.reason
            model_output['err_obj'] = str(page.raise_for_status())

        #Create bs4 object to access html elements
        soup = bs(page.content,features="lxml")
        model_output['data'] = '"' + str(soup).replace('"',"'") + '"'

        feed = soup.find('feed')
        entries=[]  # a list to store entries

        for entry in feed.find_all_next('entry'):
            # Single elements
            id = entry.id.text
            title = entry.title.text
            updated = entry.updated.text
            link_href = entry.link['href']

            # Summary contains nested elements
            summary = entry.summary
            # Summary has p with classname "quicksummary" containing multiple a tags (0 or more!)
            quicksummary = summary.find_all('p')

            num_of_reports = None
            if(len(quicksummary) > 0):
                #Quicksummary can have 0 or more p
                # print(quicksummary)
                for p in quicksummary:
                    # p can contain 0 or more a
                    a_list_titles = p.find_all('a')
                    # Go over every a element and check if the regex matches \d+\sreports 
                    # to get the number of reports if available
                    for a in a_list_titles:
                        t = a.get('title','No title attribute')
                        x = re.search("([1-9]+\sreports)", t)
                        # Only check where x exist, some return None, 
                        # remove last 8 chars which are fixed to get the number
                        if(x):
                            num_of_reports = x.group()[:-8]
                        
            # Summary has dl which contains 3 dt (Time,Location,Depth) 
            # and 4 dd (2 time 'children', 1 location 'child' and 1 depth 'child')
            dl = summary.dl

            # dt = dl.find_all('dt') # Should be a list of 3
            # print(dt)
            # time_text = dt[0].text
            # location_text = dt[1].text
            # depth_text = dt[2].text

            # Elements of interest, dt is same static text for each entry
            dd = dl.find_all('dd') # Should be a list of 4
            time_utc = dd[0].text
            time_utc_at = dd[1].text[:-13] #Time at epicenter remove text to only keep datetime string
            location_coordinates = dd[2].text
            depth_string = dd[3].text # Use regex to find km and mi to only keep the numerical parts
            depth_km = re.search('(\d+.\d+\skm)',depth_string).group()[:-3]  # Remove last 3 chars to keep the numerical value in km
            depth_mi = re.search('(\d+.\d+\smi)',depth_string).group()[:-3] # Remove last 3 chars to keep the numerical value in mi

            # Single elements
            georss_point = entry.find('georss:point').text #17.8908333333333 -66.9606666666667
            georss_elev = entry.find('georss:elev').text #-12000

            # Each category has a term element that contains the text we are interested in.
            cat_age = entry.find_all('category')[0]['term']
            cat_mag = entry.find_all('category')[1]['term']
            
            shaking = {
                1: 'Not felt',
                2: 'Weak',
                3: 'Weak',
                4: 'Light',
                5: 'Moderate',
                6: 'Strong',
                7: 'Very strong',
                8: 'Severe',
                9: 'Violent',
                10: 'Extreme'
            }

            damage = {
                1: 'None',
                2: 'None',
                3: 'None',
                4: 'None',
                5: 'Very light',
                6: 'Light',
                7: 'Moderate',
                8: 'Moderate/Heavy',
                9: 'Heavy',
                10: 'Very heavy'
            }

            cat_mag_intensity = cat_mag[-1:] # Get the magnitude digit

            #Enriched data from cat_mag_intensity, sharking and damage source from earthquake.usgs.gov
            cat_mag_shaking = shaking[int(cat_mag_intensity)] # Use magnitude_intensity to select label from the shaking dict
            cat_mag_damage = damage[int(cat_mag_intensity)] # Use magnitude_intensity to select label from the damage dict

            cat_contributor = entry.find_all('category')[2]['term']
            cat_author = entry.find_all('category')[3]['term']

            # Add all data to entries list
            entries.append([
                id,
                title,
                updated,
                link_href, 
                num_of_reports,
                time_utc,
                time_utc_at,
                location_coordinates,
                depth_string,
                depth_km,
                depth_mi,
                georss_point,
                georss_elev,
                cat_age,
                cat_mag,
                cat_mag_shaking,
                cat_mag_damage,
                cat_contributor,
                cat_author
            ])

        columns = ['id',
            'title',
            'updated',
            'link_href', 
            'num_of_reports',
            'time_utc',
            'time_utc_at_epicenter',
            'location_coordinates',
            'depth_string',
            'depth_km',
            'depth_mi',
            'georss_point',
            'georss_elev',
            'cat_age',
            'cat_mag',
            'cat_mag_shaking',
            'cat_mag_damage',
            'cat_contributor',
            'cat_author'
            ]

        # print(entries[0])

        #Convert entries list into dataframe
        df = pd.DataFrame(data=entries,columns=columns)
        model_output['execution_time_ms'] = 1000 * (datetime.now().timestamp() - datetime.strptime(model_output['timestamp'],'%Y-%m-%dT%H:%M:%S.%f').timestamp())
        return df

    #If any errors occur in the try-block we want to know what the origin is while we interact with the beautifulsoup object
    except Exception as e:
            model_output['bs_error'] = e
            model_output['execution_time_ms'] = 1000 * (datetime.now().timestamp() - datetime.strptime(model_output['timestamp'],'%Y-%m-%dT%H:%M:%S.%f').timestamp())

#Return df
df = main()
# Print out log info
print(model_output)

# Paths for saving files
path = '/home/fox/Desktop/Study/In-Progress/DataWrangling'
path_log = path + '/Project/scrape_html/logs/'
path_data = path + '/Project/scrape_html/data/'

# Save log to logs folder
file_name_log = f'log_api_earthquake_ugsg_gov_{datetime.utcnow().isoformat()}.csv'
with open(path_log+file_name_log,mode='w') as file:
    keys = list(model_output.keys())
    values = list(model_output.values())
    header = ','.join(keys) 
    row = '\n' + ','.join(map(str, values)) 
    lines = header + row
    file.write(lines)

# Save data to data folder
file_name_data = f'data_api_earthquake_ugsg_gov_{datetime.utcnow().isoformat()}.csv'
if(df is not None):
    # Write out the df to csv
    df.to_csv(path_data+file_name_data,index=False)
