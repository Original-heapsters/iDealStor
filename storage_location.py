import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

class StorageLocation:

   def __init__(self):
       print "Init"

   def hello(self):
     print "Hello storage location"

df = pd.read_csv('storage_loc1.csv')
df.head()

cases = []
colors = ['rgb(239,243,255)','rgb(189,215,231)','rgb(107,174,214)','rgb(33,113,181)']
months = {6:'June',7:'July',8:'Aug',9:'Sept'}

for i in range(6,10)[::-1]:
    cases.append( dict(
        type = 'scattergeo',
        lon = df[ df['Month'] == i ]['lon'],
        lat = df[ df['Month'] == i ]['lat'],
        text = df[ df['Month'] == i ]['Value'],
        sizemode = 'diameter',
        name = months[i],
        marker = dict(
            size = df[ df['Month'] == i ]['Value']/50,
            color = colors[i-6],
            line = dict(width = 0)
        ),
        tick0 = 0,
        zmin = 0,
        dtick = 1000,
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = ''
        ),
    ) )

cases[0]['text'] = df[ df['Month'] == 9 ]['Value'].map('{:.0f}'.format).astype(str)+' '+\
    df[ df['Month'] == 9 ]['Country']
cases[0]['mode'] = 'markers+text'
cases[0]['textposition'] = 'bottom center'

inset = [
    dict(
        type = 'choropleth',
        locationmode = 'country names',
        locations = df[ df['Month'] == 9 ]['Country'],
        z = df[ df['Month'] == 9 ]['Value'],
        text = df[ df['Month'] == 9 ]['Country'],
        colorscale = [[0,'rgb(0, 0, 0)'],[1,'rgb(0, 0, 0)']],
        autocolorscale = False,
        showscale = False,
        geo = 'geo2'
    ),
    dict(
        type = 'scattergeo',
        lon = [23],
        lat = [103],
        text = ['Mexico'],
        mode = 'text',
        showlegend = False,
        geo = 'geo2'
    )
]

layout = dict(
    title = 'Test',
    geo = dict(
        resolution = 50,
        scope = 'mexico',
        showframe = False,
        showcoastlines = True,
        showland = True,
        landcolor = "rgb(229, 229, 229)",
        countrycolor = "rgb(255, 255, 255)" ,
        coastlinecolor = "rgb(255, 255, 255)",
        projection = dict(
            type = 'Mercator'
        ),
        lonaxis = dict( range= [ -15.0, -5.0 ] ),
        lataxis = dict( range= [ 0.0, 12.0 ] ),
        domain = dict(
            x = [ 0, 1 ],
            y = [ 0, 1 ]
        )
    ),
    geo2 = dict(
        scope = 'mexico',
        showframe = False,
        showland = True,
        landcolor = "rgb(229, 229, 229)",
        showcountries = False,
        domain = dict(
            x = [ 0, 10],
            y = [ 0, 10 ]
        ),
        bgcolor = 'rgba(255, 255, 255, 0.0)',
    ),
    legend = dict(
           traceorder = 'reversed'
    )
)

fig = { 'layout':layout, 'data':cases+inset }
url = py.plot( fig, validate=False, filename='Test' )
