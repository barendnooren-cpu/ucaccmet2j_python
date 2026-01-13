#Import data
import json
import csv


#Read files
with open('precipitation.json', encoding='utf-8') as file:
    data_precipitation = json.load(file)

#Order data per station
stations = []
with open('stations.csv', encoding='utf-8') as f:
    for line in f:
        station_strings = line.strip().split(',')
        stations.append(station_strings)

#process all stations
all_results = {}
data_rows = stations[1:]


for row in data_rows:
    location = row[0]
    state = row[1]
    station_code = row[2]

    station_measurements = []
    for entry in data_precipitation:
        if entry['station'] == station_code:
            station_measurements.append(entry)

#Obtain totals per month per stations
    total_monthly = {}

    for measurement in station_measurements:
        date_string = measurement['date']
        date_parts = date_string.split('-')
        month = int(date_parts[1]) #turning month notation into integers

        precip = measurement['value']

        if month in total_monthly:
            total_monthly[month] = total_monthly[month] + precip
            
        else:
            total_monthly[month] = precip
        

    # print(f'Monthly total precipitation: {total_monthly}')

    # #Calculating yearly precipitation
    allresults_locations = []

    total_yearly_precipitation = sum(total_monthly.values())
    allresults_locations.append(total_yearly_precipitation)
    #Calculating relative monthly precipitation
    relative_monthly_precipitation = {}

    for month, monthly_total in total_monthly.items(): #Create pairs of (month, monthly total) 
    #get proportion for relative precipitation
        proportion = monthly_total/total_yearly_precipitation

        if month in relative_monthly_precipitation:
            relative_monthly_precipitation[month] = relative_monthly_precipitation[month] + proportion

        else:
            relative_monthly_precipitation[month] = proportion

    #calculate relative yearly precipitation
    total_all_stations = sum(allresults_locations)
    print(allresults_locations)
    

# #dumping results in json file
    all_results[location] = {
        "station": station_code,
        "state": state,
        "total_monthly_precipitation": list(total_monthly.values()),
        "total_yearly_precipitation": total_yearly_precipitation,
        "relative_monthly_precipitation": list(relative_monthly_precipitation.values())
            }

    with open('results.json', 'w', encoding='utf-8') as file:
        json.dump(all_results, file, indent=4, ensure_ascii=False)