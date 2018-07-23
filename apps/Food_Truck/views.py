from django.shortcuts import render, redirect

# Create your views here.

def home(request):
	return render(request, 'home.html')

def login(request):
	if trucks < 1:
		return redirect('/create/')

	return redirect('/dashboard/')

def create(request):

	return render(request, 'first_store.html')

def create_truck(request):

	return redirect('/dashboard/')

def dashboard(request):

	return render(request, 'dashboard.html')