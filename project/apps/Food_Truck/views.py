from django.shortcuts import render, redirect
import bcrypt
from .models import *
from django.contrib import messages
import pyowm
owm = pyowm.OWM('b913e1d2697f85dea1f1bd5adf0a07da')


def home(request):
	if 'id' not in request.session:
		request.session['id'] = 0
	return render(request, 'home.html')

def register_page(request):

	return render(request, 'register.html')

def register(request):
	errors = User.objects.validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/register_page/')
	else:
		hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		User.objects.create(
			nickname = request.POST['nickname'],
			email = request.POST['email'],
			password = hashpw
			)
		ID = User.objects.get(email = request.POST['email']).__dict__['id']
		request.session['id'] = ID
		print('redirect to create page')
		return redirect('/create/')


def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		print('error')
		for key, value in errors.items():
			messages.warning(request, value)
		return redirect('/')
	else:
		print('get email')
		user = User.objects.filter(email = request.POST['email'])
		if user :
			if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()) == False:
				print("invalid")
				messages.warning(request, "invalid Email or Password")
				return redirect('/')
			else:
				print('pass')
				request.session['id'] = user[0].id
				if User.objects.get(id = request.session['id']).has_truck == False:
					print('redirect to create page')
					return redirect('/create/')

				print('redirect to dash')
				return redirect('/dashboard/')
		else:
			messages.warning(request,"invalid Email or Password")
			return redirect('/')
	

def create(request):
	return render(request, 'create.html')

def create_truck(request):
	Truck.objects.create(
		name = request.POST['name'],
		owner = User.objects.get(id = request.session['id']),
		location = request.POST['location']
		)
	this_user = User.objects.get(id = request.session['id'])
	this_user.has_truck = True
	this_user.save()
	return redirect('/dashboard/')

def dashboard(request):
	observation = owm.weather_at_place('Seattle,US')
	w = observation.get_weather()
	print(w)                      # <Weather - reference time=2013-12-18 09:20,
                              # status=Clouds>
	context = {
    	"temp" : w.get_temperature('celsius')['temp'],
    	"humidity": w.get_humidity(),
    }
	# Weather details
	print(w.get_wind())                  # {'speed': 4.6, 'deg': 330}
	print(w.get_humidity())              # 87
	print(w.get_temperature('celsius'))  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

	# Search current weather observations in the surroundings of
	# lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
	return render(request, 'dashboard.html', context)


def logout(request):
	request.session.clear()

	return redirect('/')

def buy_menu(request):
	return render(request, 'buy.html', {'ingredients': Ingredient.objects.all(), 'user':User.objects.get(id=request.session['id'])})

def tools(request):
	return render(request, 'tools.html', {'ingredients':Ingredient.objects.all(), 'products':Product.objects.all()})

def add_ingredient(request):
	Ingredient.objects.create(ingredient_name=request.POST['ingredient_name'], ingredient_type=request.POST['ingredient_type'], description=request.POST['desc'], buy_price=request.POST['buy_price'])
	return redirect('/tools')

def add_product(request):
	Product.objects.create(product_name=request.POST['product_name'], product_type=request.POST['product_type'], description=request.POST['desc'], sell_price=request.POST['sell_price'])
	return redirect('/tools')

def buy_ingredient(request):
	target = Ingredient.objects.get(id=request.POST['id'])
	user = User.objects.get(id=request.session['id'])
	if user.fund - target.buy_price > 0:
		target.stock += 1
		user.fund -= target.buy_price
		target.save()
		user.save()	
	else:
		print('not enough fund')
		messages.warning(request,"Not enough money!")

	return redirect('/shopping_list')