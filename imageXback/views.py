from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def signin(request):
    template = loader.get_template('signin.html')
    return HttpResponse(template.render({}, request))

def signup(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render({}, request))

def signindata(request):
    print( request.POST )
    if signin_auth( request.POST['username'], request.POST['password'] ):
        return HttpResponse('yes')
    else:
        return redirect( signin )

def signupdata(request):
    signup_create( request.POST['username'], request.POST['password'] )
    return redirect( signin )

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def signup_create(username, password):
    User.objects.create_user(username=username, password=password).save()

def signin_auth(username, password):
    user = authenticate(username=username,password=password)

    return user != None

