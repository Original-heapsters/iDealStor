import os
import json
from type_of_food import TypeOfFood
from food_survival import FoodSurvival
from storage_location import StorageLocation
from forecast import Forecast
from flask import Flask, render_template, request, g, session
from flask.ext.googlemaps import GoogleMaps


app = Flask(__name__)
GoogleMaps(app, key="AIzaSyDnDdKk8h8ipdZFyLMBeCUSbdPcShUNQjI")
UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some key for session'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        args = []
        args.append(request.form['firstname'])
        args.append(request.form['lastname'])
        return render_template('index.html', args=args)
    else:
        return render_template('index.html')

@app.route('/type_of_food', methods=['GET','POST'])
def type_of_food():

    typeOfFood = TypeOfFood()
    typeOfFood.hello()
    crops = {}
    crops = typeOfFood.getCropJSON(os.path.abspath('./CropTypes.json'))

    if request.method == 'POST':
        args = []
        for item in request.form.getlist('crops'):
            args.append(item)
        selectedCrops = {}

        for key,value in crops.items():
            for v in value:
                for crop,cropData in v.items():
                    if cropData["name"] in args:
                        selectedCrops[crop] = {}
                        print crop
                        for tempStat in cropData["temperatures"]:
                            selectedCrops[crop][tempStat] = cropData["temperatures"][tempStat]
                        #print tempStat
                        #print cropData["temperatures"][tempStat]

        for k,v in selectedCrops.items():
            for key, val in selectedCrops[k].items():
                print k + " -- " + key + " -- " + val

        session['selectCrops'] = selectedCrops


        return render_template('type_of_food.html', args=args, crops=crops)
    else:
        if 'selectCrops' in session:
            selCrops = session['selectCrops']
            if len(selCrops) > 0:
                for k,v in selCrops.items():
                    for key, val in selCrops[k].items():
                        print "SELECTED" + k + " -- " + key + " -- " + val
        return render_template('type_of_food.html', crops=crops)


@app.route('/food_survival', methods=['GET','POST'])
def food_survival():

    foodSurvival = FoodSurvival()
    foodSurvival.hello()

    if request.method == 'POST':
        args = []
        args.append(request.form['firstname'])
        args.append(request.form['lastname'])
        return render_template('food_survival.html', args=args)
    else:
        return render_template('food_survival.html')


@app.route('/storage_location', methods=['GET','POST'])
def storage_location():

    storageLocation = StorageLocation()
    storageLocation.hello()
    #storageLocation.map()
    if request.method == 'POST':
        lat = request.form['latitude']
        long = request.form['longitude']
        args = []
        args.append(request.form['longitude'])
        args.append(request.form['latitude'])

        tempMax,tempMin,temp,humidity = storageLocation.getWeather(lat,long)
        return render_template('storage_location.html',
        args=args,
        tempMax=tempMax,
        tempMin=tempMin,
        temp=temp,
        humidity=humidity,
        lat=lat,
        long=long)
    else:
        return render_template('storage_location.html')

@app.route('/forecast', methods=['GET','POST'])
def forecast():

    forecaster = Forecast()
    forecaster.hello()

    if request.method == 'POST':
        args = []
        args.append(request.form['firstname'])
        args.append(request.form['lastname'])
        return render_template('forecast.html', args=args)
    else:
        return render_template('forecast.html')








def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True);
