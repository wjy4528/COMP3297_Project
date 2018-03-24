from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required

from . import models

from django.db.models import Q

import re

def index(request):
    return HttpResponse("Hello, world. You're at the imageX index.")

def home(request):
    template = loader.get_template('index.html')
    images = models.Image.objects.all()
    return HttpResponse(template.render({'images':images}, request))

def signin(request):
    template = loader.get_template('signin.html')
    return HttpResponse(template.render({}, request))

def signup(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render({}, request))

def search_image(request):
    search_str = request.GET['searchstring']
    template = loader.get_template('index.html')
    images = models.Image.objects.all().filter( 
        Q( category=search_str ) | Q( tags__icontains=search_str ) )

    return HttpResponse(template.render({'images':images}, request))

def my_profile(request):
    template = loader.get_template('my_profile.html')
    return HttpResponse(template.render({}, request))

def edit_profile(request):
    template = loader.get_template('edit_profile.html')
    return HttpResponse(template.render({}, request))

def all_image(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def member_image(request, memberID):
    template = loader.get_template('index.html')
    images = models.Image.objects.all().filter( uploader_id=memberID )
    return HttpResponse(template.render({'images':images}, request))

@login_required
def my_image(request):
    template = loader.get_template('my_image.html')
    images = models.Image.objects.all().filter( uploader_id=request.user.id )
    return HttpResponse(template.render({'images':images}, request))

@login_required
def upload_image_page(request):
    template = loader.get_template('upload_image.html')
    return HttpResponse(template.render({'form': None}, request))

@login_required
def upload_image_data(request):

    if request.method == 'POST':
        p_dict = dict(request.POST)
        p_dict['uploader'] = request.user.id
        p_dict['tags'] = ','.join( p_dict['tags'] )
        image_obj = models.ImageForm(p_dict, request.FILES)

        if image_obj.is_valid():
            image_obj.save()
            return HttpResponseRedirect('/')
        else:
            for field in image_obj:
                if field.errors:
                    print(field.errors)
            print( 'heyheyhey' )
            return render_to_response('upload_image.html', {'form': image_obj})
    else:
        return redirect( upload_image_page )

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def signindata(request):

    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password'])

    if user:
        login(request, user)

        return_to = request.META.get('HTTP_REFERER', False)
        if return_to:
            reobj = re.match(r'.*\?next=(.*)',return_to)
            if reobj:
                print( reobj.groups(0)[0] )
                return HttpResponseRedirect(reobj.groups(0)[0])
        
        return HttpResponseRedirect('/')
    else:
        return redirect( signin )

def signupdata(request):

    u = User.objects.create_user(
        username=request.POST['username'], 
        password=request.POST['password'])
    u.save()
    login(request, u)

    return HttpResponseRedirect('/')

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')
