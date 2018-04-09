from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from . import models

from django.db.models import Q
from django.db.models import F

import re

MAX_UPLOAD_TOTAL = 40
MAX_UPLOAD_PER_DAY = 30

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

def update_likes(request,imgID):
    models.Image.objects.filter(id=imgID).update(likes=F('likes')+1)
    return HttpResponse(request)

def update_download(request,imgID):
    models.Image.objects.filter(id=imgID).update(download=F('download')+1)
    return HttpResponse(request)

def search_image(request):
    search_str = request.GET['searchstring']
    template = loader.get_template('index.html')
    images = models.Image.objects.all().filter( 
        Q( category=search_str.lower() ) | Q( tags__icontains=search_str )  | Q( description__icontains=search_str ) )

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

def delete_image(request, imgID):
    #template = loader.get_template('index.html')
    models.Image.objects.all().filter( id=imgID ).delete()
    return HttpResponse(request)


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
        try:
            p_dict = dict(request.POST)
            p_dict['uploader'] = request.user.id
            p_dict['tags'] = ' '.join( p_dict['tags'] )
            p_dict['category'] = p_dict['category'][0].lower()
            #print(p_dict)
            #print(p_dict['description'])
            p_dict['description'] = ' '.join( p_dict['description'])

        except KeyError:
            return redirect( upload_image_page )

        '''
        if len(p_dict['tags'])==0:
            p_dict['tags']="None"

        if len(p_dict['description'])==0:
            p_dict['description']="None"

        if len(p_dict['category'])==0:
            p_dict['category']="None"
        '''
        if p_dict['tags'].count(' ')>9:
            messages.add_message(request, messages.INFO, 'You can select at most ten tags!')
            return render(request, 'upload_image.html')
        else:
            user_db = models.Member.objects.get(id=request.user.id)

            print( user_db.id )

            if user_db.uploadCount >= MAX_UPLOAD_TOTAL:
                messages.add_message(request, messages.INFO, 'You have reached your total upload limitation!')
                return render(request, 'upload_image.html')

            today = datetime.datetime.now().date()

            if models.Image.objects.filter(
                    uploader=request.user.id,
                    uploadedOn__gte=today
                ).count() >= MAX_UPLOAD_PER_DAY:
                messages.add_message(request, messages.INFO, 'You have reached your daily upload limitation!')
                return render(request, 'upload_image.html')

            image_obj = models.ImageForm(p_dict, request.FILES)

            if image_obj.is_valid():
                image_obj.save()

                user_db.uploadCount += 1
                user_db.save()
                return HttpResponseRedirect('/')
            else:
                '''
                for field in image_obj:
                    if field != 'description':
                        if field != 'tags':
                            if field.errors:
                                print(field.errors)

                return render_to_response('upload_image.html', {'form': image_obj})
                '''
                messages.add_message(request, messages.INFO, 'You must select at least one Image!')
                return render(request, 'upload_image.html')

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
                return HttpResponseRedirect(reobj.groups(0)[0])

        return HttpResponseRedirect('/home')
    else:
        messages.add_message(request, messages.INFO, 'Wrong Password or Username!')
        return render(request, 'signin.html')

def signupdata(request):
    if User.objects.filter(username=request.POST['username']).exists():
        messages.add_message(request, messages.INFO, 'Too slow! Username has been registered!')
        return render(request, 'signup.html')
    elif (request.POST['confirm_password']!=request.POST['password']):
        messages.add_message(request, messages.INFO, 'Password must be the same!')
        return render(request, 'signup.html')

    # success scenario
    u = User.objects.create_user(
        username=request.POST['username'], 
        password=request.POST['password'])

    m = models.Member.objects.create(
        user=u,
        username=request.POST['username'])

    u.save()
    m.save()

    login(request, u)

    return HttpResponseRedirect('/')

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')
