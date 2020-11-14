import requests
from flask import Flask, render_template, request,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather'

db = SQLAlchemy(app)

class City(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50),nullable=False)


@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		new_city = request.form.get('city')
		if new_city and City.query.filter_by(name=new_city).first()==None:
			new_city_obj = City(name=new_city)
			db.session.add(new_city_obj)
			db.session.commit()

		delete_city = request.form.get('delete')
		if delete_city:
			delete_city_obj = City.query.filter_by(name=delete_city).first()
			db.session.delete(delete_city_obj)
			db.session.commit()
			print(delete_city)



	cities = City.query.all()

	API_KEY = 'a919dd84e84670055aee630306f569a0'
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID='
	url += API_KEY
	
	weather_data = []

	show_msg = 1

	for city in reversed(cities):

		r = requests.get(url.format(city.name)).json()
		
		print(r)

		if r['cod'] != '404':
			weather = {
		    'city': city.name,
		    'temperature': int(r['main']['temp']) ,
		    'description': r['weather'][0]['description'],
		    'icon': r['weather'][0]['icon'],

		     } 
			weather_data.append(weather)
		else:
			show_msg = 1
			flash('The city could not be found!')
			delete_city_obj = City.query.filter_by(name=city.name).first()
			db.session.delete(delete_city_obj)
			db.session.commit()


	return render_template('index.html', weather_data=weather_data)
