import requests
import json

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

        return (avgMax, avgMin, avgTemp, avgHumidity)



    def k2f(self,t):
        return (t*9/5.0)-459.67
