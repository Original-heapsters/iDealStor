import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *
import pandas as pd
import requests
import os
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
        df = pd.read_csv('out.csv')
        df.head()
        limits = [(0,19),(20,60),(61,90),(91,150),(151,200)]
        colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
        Ideal_Colors = ["rgb(244,164,96)","rgb(255,0,255)","rgb(255,255,0)","rgb(124,252,0)"]
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

        if 'wheat' in df.columns and 'rice' in df.columns and 'corn' in df.columns:
            data = go.Data([
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Humidity',
                    marker=Marker(
                        size=df['Avg_Humidity']/10,
                        color='rgb(124,252,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Humidity'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Temp',
                    marker=Marker(
                        size=df['Avg_Temp']/10,
                        color='rgb(255,20,147)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Max Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Max']/10,
                        color='rgb(255,0,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Max'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Min Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Min']/10,
                        color='rgb(30,144,255)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Min'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Wheat Ideal Score',
                    marker=Marker(
                        size=df['wheat'] * 5,
                        color=Ideal_Colors[0],
                        opacity=0.7
                    ),
                    text=df['wheat'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Rice Ideal Score',
                    marker=Marker(
                        size=df['rice'] * 5,
                        color=Ideal_Colors[1],
                        opacity=0.7
                    ),
                    text=df['rice'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Corn Ideal Score',
                    marker=Marker(
                        size=df['corn'] * 5,
                        color=Ideal_Colors[2],
                        opacity=0.7
                    ),
                    text=df['corn'],
                    hoverinfo='text'
                )]
            )
            layout = dict(
                    font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'),
                    title = 'Ideal Storage Areas',
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
            fig = dict( data=data, layout=layout )
            py.plot( fig, validate=False, filename='Avg_Temp', auto_open=False )

        elif 'wheat' in df.columns and 'rice' in df.columns:
            data = go.Data([
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Humidity',
                    marker=Marker(
                        size=df['Avg_Humidity']/10,
                        color='rgb(124,252,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Humidity'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Temp',
                    marker=Marker(
                        size=df['Avg_Temp']/10,
                        color='rgb(255,20,147)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Max Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Max']/10,
                        color='rgb(255,0,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Max'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Min Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Min']/10,
                        color='rgb(30,144,255)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Min'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Wheat Ideal Score',
                    marker=Marker(
                        size=df['wheat'] * 5,
                        color=Ideal_Colors[0],
                        opacity=0.7
                    ),
                    text=df['wheat'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Rice Ideal Score',
                    marker=Marker(
                        size=df['rice'] * 5,
                        color=Ideal_Colors[1],
                        opacity=0.7
                    ),
                    text=df['rice'],
                    hoverinfo='text'
                )]
            )
            layout = dict(
                    font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'),
                    title = 'Ideal Storage Areas',
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
            fig = dict( data=data, layout=layout )
            py.plot( fig, validate=False, filename='Avg_Temp', auto_open=False )

        elif 'wheat' in df.columns and 'corn' in df.columns:
            data = go.Data([
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Humidity',
                    marker=Marker(
                        size=df['Avg_Humidity']/10,
                        color='rgb(124,252,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Humidity'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Temp',
                    marker=Marker(
                        size=df['Avg_Temp']/10,
                        color='rgb(255,20,147)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Max Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Max']/10,
                        color='rgb(255,0,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Max'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Min Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Min']/10,
                        color='rgb(30,144,255)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Min'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Wheat Ideal Score',
                    marker=Marker(
                        size=df['wheat'] * 5,
                        color=Ideal_Colors[0],
                        opacity=0.7
                    ),
                    text=df['wheat'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Corn Ideal Score',
                    marker=Marker(
                        size=df['corn'] * 5,
                        color=Ideal_Colors[2],
                        opacity=0.7
                    ),
                    text=df['corn'],
                    hoverinfo='text'
                )]
            )
            layout = dict(
                    font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'),
                    title = 'Ideal Storage Areas',
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
            fig = dict( data=data, layout=layout )
            py.plot( fig, validate=False, filename='Avg_Temp', auto_open=False )

        elif 'corn' in df.columns and 'rice' in df.columns:
            data = go.Data([
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Humidity',
                    marker=Marker(
                        size=df['Avg_Humidity']/10,
                        color='rgb(124,252,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Humidity'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Temp',
                    marker=Marker(
                        size=df['Avg_Temp']/10,
                        color='rgb(255,20,147)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Max Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Max']/10,
                        color='rgb(255,0,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Max'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Min Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Min']/10,
                        color='rgb(30,144,255)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Min'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Corn Ideal Score',
                    marker=Marker(
                        size=df['corn'] * 5,
                        color=Ideal_Colors[2],
                        opacity=0.7
                    ),
                    text=df['corn'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Rice Ideal Score',
                    marker=Marker(
                        size=df['rice'] * 5,
                        color=Ideal_Colors[1],
                        opacity=0.7
                    ),
                    text=df['rice'],
                    hoverinfo='text'
                )]
            )
            layout = dict(
                    font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'),
                    title = 'Ideal Storage Areas',
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
            fig = dict( data=data, layout=layout )
            py.plot( fig, validate=False, filename='Avg_Temp', auto_open=False )

        elif 'corn' in df.columns:
            data = go.Data([
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Humidity',
                    marker=Marker(
                        size=df['Avg_Humidity']/10,
                        color='rgb(124,252,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Humidity'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Temp',
                    marker=Marker(
                        size=df['Avg_Temp']/10,
                        color='rgb(255,20,147)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Max Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Max']/10,
                        color='rgb(255,0,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Max'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Min Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Min']/10,
                        color='rgb(30,144,255)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Min'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Corn Ideal Score',
                    marker=Marker(
                        size=df['corn'] * 5,
                        color=Ideal_Colors[2],
                        opacity=0.7
                    ),
                    text=df['corn'],
                    hoverinfo='text'
                )]
            )
            layout = dict(
                    font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'),
                    title = 'Ideal Storage Areas',
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
            fig = dict( data=data, layout=layout )
            py.plot( fig, validate=False, filename='Avg_Temp', auto_open=False )

        elif 'rice' in df.columns:
            data = go.Data([
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Humidity',
                    marker=Marker(
                        size=df['Avg_Humidity']/10,
                        color='rgb(124,252,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Humidity'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Temp',
                    marker=Marker(
                        size=df['Avg_Temp']/10,
                        color='rgb(255,20,147)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Max Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Max']/10,
                        color='rgb(255,0,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Max'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Min Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Min']/10,
                        color='rgb(30,144,255)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Min'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Rice Ideal Score',
                    marker=Marker(
                        size=df['rice'] * 5,
                        color=Ideal_Colors[1],
                        opacity=0.7
                    ),
                    text=df['rice'],
                    hoverinfo='text'
                )]
            )
            layout = dict(
                    font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'),
                    title = 'Ideal Storage Areas',
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
            fig = dict( data=data, layout=layout )

        elif 'wheat' in df.columns:
            data = go.Data([
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Humidity',
                    marker=Marker(
                        size=df['Avg_Humidity']/10,
                        color='rgb(124,252,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Humidity'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Temp',
                    marker=Marker(
                        size=df['Avg_Temp']/10,
                        color='rgb(255,20,147)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Max Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Max']/10,
                        color='rgb(255,0,0)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Max'],
                    hoverinfo='text'
                ),Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='AVG Min Temp',
                    marker=Marker(
                        size=df['Avg_Temp_Min']/10,
                        color='rgb(30,144,255)',
                        opacity=0.7
                    ),
                    text=df['Avg_Temp_Min'],
                    hoverinfo='text'
                ),
                Scattermapbox(
                    lat=df['Latitude'],
                    lon=df['Longitude'],
                    mode='markers',
                    name='Wheat Ideal Score',
                    marker=Marker(
                        size=df['wheat'] * 5,
                        color=Ideal_Colors[0],
                        opacity=0.7
                    ),
                    text=df['wheat'],
                    hoverinfo='text'
                )]
            )
            layout = dict(
                    font=dict(family='Courier New, monospace', size=24, color='#7f7f7f'),
                    title = 'Ideal Storage Areas',
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
            fig = dict( data=data, layout=layout )
            py.plot( fig, validate=False, filename='Avg_Temp', auto_open=False )




        # layout = dict(
        #         title = 'Ideal Storage Areas',
        #         showlegend = True,
        #         geo = dict(
        #             scope='world',
        #             showcontries= True,
        #             projection=dict( type='Robinson' ),
        #             showland = True,
        #             mapscale = 1,
        #             landcolor = 'rgb(217, 217, 217)',
        #             subunitwidth=2,
        #             countrywidth=2,
        #             subunitcolor="rgb(255, 255, 255)",
        #             countrycolor="rgb(255, 255, 255)"
        #         ),
        #     )
        # fig = dict( data=data, layout=layout )
        # py.plot( fig, validate=False, filename='Avg_Temp', auto_open=False )
        #return (avgMax, avgMin, avgTemp, avgHumidity)
        #py.plot( fig, validate=False, filename='Avg_Temp', auto_open=False )


    def getIdealScores(self, cropDict):
        deEfs = []
        endDict = {}
        for crops in cropDict:
            newDict = {}
            tempList = []
            print crops
            endDict[str(crops)] = []
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
                        if self.acceptable(line['Avg_Temp'], data[0], 10):
                            idealCount += 1
                        if self.acceptable(line['Avg_Temp_Min'], data[1], 10):
                            idealCount += 1
                        if self.acceptable(line['Avg_Temp_Max'], data[2], 10):
                            idealCount += 1
                        if self.acceptable(line['Avg_Humidity'], data[3], 10):
                            idealCount += 1
                        endDict[item].append(str(idealCount))
            headerList = ['index']
            for key,value in endDict.items():
                headerList.append(key)
                #print(line['giLatitude'], line['Longitude'], line['Avg_Humidity'], line['Avg_Temp'], line['Avg_Temp_Max'], line['Avg_Temp_Min'])
                #creates DataFrame from the endDict
            dicti = pd.DataFrame(endDict)
            dicti.to_csv("dfEndDic.csv")

            inputFileName = "dfEndDic.csv"
            outputFileName = os.path.splitext(inputFileName)[0] + "_modified.csv"

            with open(inputFileName, 'rb') as inFile, open(outputFileName, 'wb') as outfile:
                r = csv.reader(inFile)
                w = csv.writer(outfile)

                next(r, None)  # skip the first row from the reader, the old header
                # write new header
                w.writerow(headerList)
                # copy the rest
                for row in r:
                    w.writerow(row)

            data = pd.read_csv('dfEndDic_modified.csv')
            data1 = pd.read_csv('MOCK_DATA.csv')
            out = data.join(data1, on='index',how='left',lsuffix='_left')
            out.to_csv('out.csv')



    # def idealCsv():
    #     with open('dict.csv', 'wb') as csv_file:
    #         writer = csv.writer(csv_file)
    #         for key, value in dictionary.items():
    #             writer.writerow([key, value])
    #     with open('dict.csv', 'rb') as csv_file:
    #         reader = csv.reader(csv_file)
    #         dictionary = dict(reader)
    #         print done

    def acceptable(self, val1, val2, thresh):
        if abs(int(val1) - int(val2)) < thresh:
            return True
        else:
            return False

    def k2f(self,t):
        return (t*9/5.0)-459.67
