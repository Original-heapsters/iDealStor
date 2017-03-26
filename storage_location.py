import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

class StorageLocation:

   def __init__(self):
       print "Init"

   def hello(self):
     print "Hello storage location"

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
                #size = df_sub['Avg_Temp']/scale,
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
                projection=dict( type='equirectangular' ),
                showland = True,
                landcolor = 'rgb(217, 217, 217)',
                subunitwidth=1,
                countrywidth=1,
                subunitcolor="rgb(255, 255, 255)",
                countrycolor="rgb(255, 255, 255)"
            ),
        )
    fig = dict( data=cities, layout=layout )
    py.iplot( fig, validate=False, filename='Avg_Temp' )
