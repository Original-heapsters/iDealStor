import json

class TypeOfFood:
    def __init__(self):
        print "Init"

    def hello(self):
        print "Hello type of food"

    def getCropCSV(self, filename):
        print "Getting crop csv"
        with open(filename) as data_file:
            return json.loads(data_file)

    def getCropJSON(self, filename):
        print "Getting crop json from " + filename
        with open(filename) as data_file:

            data = json.load(data_file)
        return data
