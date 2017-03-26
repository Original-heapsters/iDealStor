from type_of_food import TypeOfFood
from food_survival import FoodSurvival
from storage_location import StorageLocation
from forecast import Forecast
from flask import Flask, render_template, request


app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    if request.method == 'POST':
        args = []
        args.append(request.form['firstname'])
        args.append(request.form['lastname'])
        return render_template('type_of_food.html', args=args)
    else:
        return render_template('type_of_food.html')


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
    storageLocation.map()
    if request.method == 'POST':
        args = []
        args.append(request.form['firstname'])
        args.append(request.form['lastname'])
        return render_template('storage_location.html', args=args)

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
