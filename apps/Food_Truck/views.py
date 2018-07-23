from django.shortcuts import render, redirect
import bcrypt
from .models import *
from django.contrib import messages
# Create your views here.

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

	return render(request, 'dashboard.html')


def logout(request):
	request.session.clear()

	return redirect('/')