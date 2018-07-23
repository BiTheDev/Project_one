from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
	def validator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['first_name']) < 2:
			errors['first_name'] = 'First name needs at least three letters.'
		if len(postData['first_name']) < 1:
			errors['first_name'] = 'First name cannot be blank.'
		elif re.search('\d+', postData['first_name']):
			errors['first_name'] ='Name cannot contain number'
		if len(postData['last_name']) < 1:
			errors['last_name'] = 'Last name needs at least three letters'
		if len(postData['last_name']) < 1:
			errors['last_name'] = 'Last name cannot be blank.'
		elif re.search('\d+', postData['last_name']):
			errors['last_name'] ='Name cannot contain number'
		if len(postData['email']) <1:
			errors['email'] = 'Email cannot be blank.'
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email'] = 'Please input correct email format.'
		if len(postData['password']) < 7:
			errors['password'] = 'Password must be no fewer than 8 characters'
		if len(postData['password']) < 1:
			errors['password'] = 'Password cannot be blank.'
		if len(postData['confirm']) < 1:
			errors['confirm'] = 'Please reconfirm your password.'
		if postData['password'] != postData['confirm']:
			errors['not_matched'] = 'Password and password confirmation does not match.'

		existing_users = User.objects.filter(email=postData['email'])
		if len(existing_users) > 0:
			errors['email'] = 'Email already registered!'

		return errors

class User(models.Model):
	nickname = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	fund = models.IntegerField()
	objects=UserManager()

class Truck():
	name = models.CharField(max_length=30)
	owner = models.ForeignKey(User, related_name='trucks')
	location = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)


class Product(models.Model):
	product_name = models.CharField(max_length=255)
	product_type = models.CharField(max_length=255)
	price = models.FloatField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
