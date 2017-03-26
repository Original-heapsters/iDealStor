import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import requests
import json
import csv

class StorageLocation:

    def __init__(self):
        print "Init"

    def hello(self):
      print "Hello storage location"

    def getWeather(self, lat, long):
        endpoint = "http://api.openweathermap.org/data/2.5/weather?appid=d683bede5d06354f220db21f1a7f8a94"
        latReq = "&lat=" + lat
        longReq = "&lon=" + long
        print '\n\n\n\n ' + endpoint + latReq + longReq

        r = requests.get(endpoint + latReq + longReq)
        max,min,temp,hum = self.getTemps(json.loads(r.text))


        return max,min,temp,hum

    def getTemps(self, data):
        print data
        max = self.k2f(data["main"]["temp_max"])
        min = self.k2f(data["main"]["temp_min"])
        temp = self.k2f(data["main"]["temp"])
        humidity = self.k2f(data["main"]["humidity"])

        return (max, min, temp, humidity)

    def getTempsAV(self, data):
        maxes = []
        mins = []
        temps = []
        humidities = []
        avgMax = 0
        avgMin = 0
        avgTemp = 0
        avgHumidity = 0
        count = 0
        for entry in data["list"]:
            avgMax += entry["main"]["temp_max"]
            avgMin += entry["main"]["temp_min"]
            avgTemp += entry["main"]["temp"]
            avgHumidity += entry["main"]["humidity"]
            count += 1
        avgMax /= count
        avgMin /= count
        avgTemp /= count
        avgHumidity /= count
        print avgMax
        print avgMin
        print avgTemp
        print avgHumidity

        avgMax = self.k2f(avgMax)
        avgMin = self.k2f(avgMin)
        avgTemp = self.k2f(avgTemp)
        avgHumidity = self.k2f(avgHumidity)

    def map(self):
        df = pd.read_csv('MOCK_DATA.csv')
        df.head()
        limits = [(0,19),(20,60),(61,90),(91,150),(151,200)]
        colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
        cities = []
        scale = 5000

        for i in range(len(limits)):
            lim = limits[i]
            df_sub = df[lim[0]:lim[1]]
            city = dict(
                type = 'scattergeo',
                locationmode = 'ISO-3',
                lon = df_sub['Longitude'],
                lat = df_sub['Latitude'],
                text = df_sub['Avg_Temp'],
                marker = dict(
                    size = df['Avg_Temp'],
                    color = colors[i],
                    line = dict(width=0.5, color='rgb(40,40,40)'),
                    sizemode = 'area'
                ),
                name = '{0} - {1}'.format(lim[0],lim[1]) )
            cities.append(city)

        layout = dict(
                title = 'Avg Temp Test',
                showlegend = True,
                geo = dict(
                    scope='world',
                    showcontries= True,
                    projection=dict( type='Robinson' ),
                    showland = True,
                    mapscale = 1,
                    landcolor = 'rgb(217, 217, 217)',
                    subunitwidth=2,
                    countrywidth=2,
                    subunitcolor="rgb(255, 255, 255)",
                    countrycolor="rgb(255, 255, 255)"
                ),
            )
        fig = dict( data=cities, layout=layout )
        py.iplot( fig, validate=False, filename='Avg_Temp' )
        return (avgMax, avgMin, avgTemp, avgHumidity)


    def getIdealScores(self, cropDict):
        deEfs = []
        for crops in cropDict:
            newDict = {}
            tempList = []
            print crops
            for crop in cropDict[crops]:
                tempList.append(cropDict[crops][crop])
                print cropDict[crops][crop]
            newDict[crops] = tempList

        deEfs.append(newDict)

        with open('MOCK_DATA.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                idealCount = 0
                for crop in deEfs:
                    for item,data in crop.items():
                        if self.acceptable(line['Avg_Temp'], data[0], 25):
                            idealCount += 1
                        if self.acceptable(line['Avg_Temp_Min'], data[1], 25):
                            idealCount += 1
                        if self.acceptable(line['Avg_Temp_Max'], data[2], 25):
                            idealCount += 1
                        if self.acceptable(line['Avg_Humidity'], data[3], 25):
                            idealCount += 1
                        print 'IdealScore ' + str(idealCount)
                #print(line['giLatitude'], line['Longitude'], line['Avg_Humidity'], line['Avg_Temp'], line['Avg_Temp_Max'], line['Avg_Temp_Min'])



    def acceptable(self, val1, val2, thresh):
        if abs(int(val1) - int(val2)) < thresh:
            return True
        else:
            return False

    def k2f(self,t):
        return (t*9/5.0)-459.67
