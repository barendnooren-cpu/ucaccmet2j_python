#Import data
import json
import csv


#Read files
with open('precipitation.json', encoding='utf-8') as file:
    data_precipitation = json.load(file)

#filter for seattle measurements
seattle_station = 'GHCND:US1WAKG0038'
seattle_measurements = []
    
for entry in data_precipitation:
    if entry['station'] == seattle_station:
        seattle_measurements.append(entry)

print(f'In Seattle, {len(seattle_measurements)} have been taken')

#filter for seattle measurements per month
total_monthly = {}

for measurement in seattle_measurements:
    date_string = measurement['date']
    date_parts = date_string.split('-')
    month = int(date_parts[1]) #turning month notation into integers

    precip = measurement['value']

    if month in  total_monthly:
        total_monthly[month] = total_monthly[month] + precip
        
    else:
        total_monthly[month] = precip
    

print(f'Monthly total precipitation: {total_monthly}')

#dumping results in json file
data = {
            "Seattle": {
    "station": 'GHCND:US1WAKG0038',
    "state": "WA",
    "total_monthly_precipitation": [total_monthly],
  
    }

}

with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)