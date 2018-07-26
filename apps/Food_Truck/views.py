from django.shortcuts import render, redirect
import bcrypt
from .models import *
from django.contrib import messages
import requests
import datetime

now = datetime.datetime.now()

def home(request):
	if 'id' not in request.session:
		request.session['id'] = 0
		request.session['truck_id'] = 0
		request.session['temperature'] = 0
		request.session['temperature'] = ''
	return render(request, 'home.html')


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

	return render(request, 'create.html', {'locations': Location.objects.all()})

def create_truck(request):
	Truck.objects.create(
		name = request.POST['name'],
		owner = User.objects.get(id = request.session['id']),
		location = Location.objects.get(id=request.POST['location'])
		)
	this_user = User.objects.get(id = request.session['id'])
	this_user.has_truck = True
	this_user.save()
	return redirect('/dashboard/')

def dashboard(request):
	api_key = 'b913e1d2697f85dea1f1bd5adf0a07da'
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid='+ api_key
	city = User.objects.get(id=request.session['id']).trucks.first().location.location_name
	city_weather = requests.get(url.format(city)).json()
	context = {
        'city' : city,
        'temperature' : city_weather['main']['temp'],
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon'],
		'date' : now.strftime("%Y/%m/%d"),
		'locations' : Location.objects.all(),
		'user': User.objects.get(id=request.session['id'])
    }
	request.session['temperature'] = city_weather['main']['temp']

	request.session['weather'] = city_weather['weather'][0]['main']
	request.session['truck_id'] = User.objects.get(id=request.session['id']).trucks.first().id
	target = User.objects.get(id=request.session['id'])
	target.last_log = datetime.datetime.now()
	print(target.last_log)
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
	cost = 0
	target = Product(product_name=request.POST['product_name'])
	target.product_type = request.POST['product_type']
	target.description = request.POST['desc']
	target.sell_price = request.POST['sell_price']
	if request.POST['ingredient_B'] == '':
		target.ingredient_B = None
	else:
		target.ingredient_B = Ingredient.objects.get(id=int(request.POST['ingredient_B']))
		cost += target.ingredient_B.buy_price
	if request.POST['ingredient_C'] == '':
		target.ingredient_C = None
	else:
		target.ingredient_C = Ingredient.objects.get(id=int(request.POST['ingredient_C']))
		cost += target.ingredient_C.buy_price
	if request.POST['ingredient_D'] == '':
		target.ingredient_D = None
	else:
		target.ingredient_D = Ingredient.objects.get(id=int(request.POST['ingredient_D']))
		cost += target.ingredient_D.buy_price
	target.ingredient_A = Ingredient.objects.get(id=int(request.POST['ingredient_A']))
	cost += target.ingredient_A.buy_price
	target.cost = cost


	target.save()
	
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
		messages.warning(request,"Not enough money!")

	return redirect('/shopping_list')

def buy10_ingredient(request):
	target = Ingredient.objects.get(id=request.POST['id'])
	user = User.objects.get(id=request.session['id'])
	if user.fund - target.buy_price * 10 > 0:
		target.stock += 10
		user.fund -= target.buy_price *9.5
		target.save()
		user.save()	
	else:
		messages.warning(request,"Not enough money!")

	return redirect('/shopping_list')

def cook(request):
	return render(request, 'cook.html' , {'products':Product.objects.all(), 'ingredients':Ingredient.objects.all()})

def make_food(request):
	target = Product.objects.get(id=request.POST['id'])
	target.stock += 1
	if target.ingredient_A.stock-1 == -1:
		messages.warning(request,"Not enough ingredients!")
		return redirect('/cook')
	else:
		target.ingredient_A.stock -=1
		target.ingredient_A.save()

	
	if target.ingredient_B != None:
		if target.ingredient_B.stock-1 == -1:
			messages.warning(request,"Not enough ingredients!")
			return redirect('/cook')
		else:
			target.ingredient_B.stock -=1
			target.ingredient_B.save()
	
	if target.ingredient_C != None:
		if target.ingredient_B.stock-1 == -1:
			messages.warning(request,"Not enough ingredients!")
			return redirect('/cook')
		else:
			target.ingredient_C.stock -=1
			target.ingredient_C.save()
	
	if target.ingredient_D != None:
		if target.ingredient_B.stock-1 == -1:
			messages.warning(request,"Not enough ingredients!")
			return redirect('/cook')
		else: 
			target.ingredient_D.stock -=1
			target.ingredient_D.save()
	
	target.save()
	return redirect('/cook')

def make10_food(request):
	target = Product.objects.get(id=request.POST['id'])
	target.stock += 10
	if target.ingredient_A.stock-10 < -1:
		messages.warning(request,"Not enough ingredients!")
		return redirect('/cook')
	else:
		target.ingredient_A.stock -=10
		target.ingredient_A.save()

	
	if target.ingredient_B != None:
		if target.ingredient_B.stock-10 < -1:
			messages.warning(request,"Not enough ingredients!")
			return redirect('/cook')
		else:
			target.ingredient_B.stock -=10
			target.ingredient_B.save()
	
	if target.ingredient_C != None:
		if target.ingredient_B.stock-10 < -1:
			messages.warning(request,"Not enough ingredients!")
			return redirect('/cook')
		else:
			target.ingredient_C.stock -=10
			target.ingredient_C.save()
	
	if target.ingredient_D != None:
		if target.ingredient_B.stock-10 < -1:
			messages.warning(request,"Not enough ingredients!")
			return redirect('/cook')
		else: 
			target.ingredient_D.stock -=10
			target.ingredient_D.save()
	
	target.save()
	return redirect('/cook')


def sell(request):
	print('Sell cycle triggered!')
	revenue = 0
	target_report = Product.objects.exclude(stock = 0)
	target_breakfast = Product.objects.exclude(stock = 0).filter(product_type='breakfast')
	target_meal = Product.objects.exclude(stock = 0).filter(product_type='meal')
	target_snack = Product.objects.exclude(stock = 0).filter(product_type='snack')
	target_drink = Product.objects.exclude(stock = 0).filter(product_type='drink')
	user = User.objects.get(id=request.session['id'])
	location = User.objects.get(id=request.session['id']).trucks.first().location
	
	# Upgrade and other modifiers
	
	if request.session['temperature'] > 100:
		location.demand_drink *= 1.4
	elif request.session['temperature'] > 90:
		location.demand_drink *= 1.2
	elif request.session['temperature'] > 80:
		location.demand_drink *= 1.1

	if request.session['weather'] == 'Rain':
		location.demand_breakfast *= 0.8
		location.demand_drink *= 0.8
		location.demand_meal *= 0.8
		location.demand_snack *= 0.8

	if request.session['weather'] == 'Snow':
		location.demand_breakfast *= 0.8
		location.demand_drink *= 0.8
		location.demand_meal *= 0.8
		location.demand_snack *= 0.8
		
	if request.session['weather'] == 'Thunderstorm':
		location.demand_breakfast *= 0.2
		location.demand_drink *= 0.2
		location.demand_meal *= 0.2
		location.demand_snack *= 0.2
	
	if request.session['weather'] == 'Drizzle':
		location.demand_breakfast *= 0.9
		location.demand_drink *= 0.9
		location.demand_meal *= 0.9
		location.demand_snack *= 0.9
		
	# data to keep track of to generate report
	cost = 0
	revenue_report = 0
	profit = 0
	item_sold = 0
	item_unsold = 0

	for items in target_report:
		item_unsold += items.stock

	for target in target_breakfast:
		if location.demand_breakfast > 0:
			location.demand_breakfast -= target.stock
			revenue = target.stock * target.sell_price
			revenue_report += target.stock * target.sell_price
			cost =+ target.stock * target.cost
			item_sold += target.stock
			target.stock = 0
			target.save()
			user.fund += revenue

	for target in target_meal:
		if location.demand_meal > 0:
			location.demand_meal -= target.stock
			revenue = target.stock * target.sell_price
			revenue_report += target.stock * target.sell_price
			cost =+ target.stock * target.cost
			item_sold += target.stock
			target.stock = 0
			target.save()
			user.fund += revenue
	

	for target in target_snack:
		if location.demand_snack > 0:
			location.demand_snack -= target.stock
			revenue = target.stock * target.sell_price
			revenue_report += target.stock * target.sell_price
			cost =+ target.stock * target.cost
			item_sold += target.stock
			target.stock = 0
			target.save()
			user.fund += revenue


	for target in target_drink:
		if location.demand_drink > 0:
			location.demand_drink -= target.stock
			revenue = target.stock * target.sell_price
			revenue_report += target.stock * target.sell_price
			cost =+ target.stock * target.cost
			item_sold += target.stock
			target.stock = 0
			target.save()
			user.fund += revenue

	for target in target_report:
		target.stock = 0

	user.age += 1
	item_unsold -= item_sold
	profit = revenue - cost
	Report.objects.create(owner=user ,cost=cost, profit=profit, revenue=revenue,item_sold=item_sold,item_unsold=item_unsold)
	user.save()
	return redirect('/dashboard')

def move(request):
	target = Truck.objects.get(id=request.session['truck_id'])
	user = User.objects.get(id=request.session['id'])
	if User.objects.get(id=request.session['id']).fund < 100:
		messages.warning(request, 'Not enough money to move!')
	if target.location == Location.objects.get(id=request.POST['location']):
		messages.warning(request, 'You are already at that location!')
	else:
		user.fund -= 100
		target.location = Location.objects.get(id=request.POST['location'])
		target.save()
		user.save()
	return redirect('/dashboard')

def report(request):

	return render(request, 'report.html', {'reports': Report.objects.filter(owner=User.objects.get(id=request.session['id'])).last()})

def upgrade(request):

	return render(request, 'upgrade.html', {'upgrades': Upgrade.objects.all()})	

def add_improvement(request):
	Upgrade.objects.create(name=request.POST['name'])
	return redirect('/upgrade')

def leaderboard(request):
	return render(request, 'leaderboard.html', {'users': User.objects.all()})
