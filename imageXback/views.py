from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from . import models
from . import sendmail
from . import settings

from django.db.models import Q
from django.db.models import F

import re
import os
import random
import string
import mimetypes

MAX_UPLOAD_TOTAL = 30
MAX_UPLOAD_PER_DAY = 40

BASE64_string = string.ascii_letters + string.digits + '+.'

TAG_SEP = ','

def get_token(sz=32):
    return ''.join([random.choice(BASE64_string) for _ in range(sz)])

def generate_password(sz=8):
    return get_token(sz=8)

def index(request):
    return HttpResponse("Hello, world. You're at the imageX index.")

def home(request):
    template = loader.get_template('index.html')
    images = models.Image.objects.all()

    for img in images:
        img.uploadedOn = img.uploadedOn.strftime("%y%m%d-%H%M%S")

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

    try:
        u_obj = models.User.objects.get(username=search_str)
        uid = u_obj.id
    except Exception as err:
        print(err )
        uid = -1

    images = models.Image.objects.all().filter( 
        Q( category__iexact=search_str ) | Q( tags__icontains=search_str )  | Q(uploader=uid)) 

    for img in images:
        img.uploadedOn = img.uploadedOn.strftime("%y%m%d-%H%M%S")

    return HttpResponse(template.render({'images':images}, request))

def my_profile(request):
    template = loader.get_template('my_profile.html')

    mem_obj = models.Member.objects.get(user=request.user.id)

    style_obj = {
        "its_me":True,
        "email":mem_obj.email,
        "description":mem_obj.description,
        "username":mem_obj.username,
    }

    return HttpResponse(template.render(style_obj, request))

def edit_profile(request):
    template = loader.get_template('edit_profile.html')

    mem_obj = models.Member.objects.get(user=request.user.id)

    style_obj = {
        "its_me":True,
        "email":mem_obj.email,
        "description":mem_obj.description,
        "username":mem_obj.username,
    }

    return HttpResponse(template.render(style_obj, request))

def all_image(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def member_image(request, memberID):
    template = loader.get_template('index.html')
    images = models.Image.objects.all().filter( uploader_id=memberID )
    return HttpResponse(template.render({'images':images}, request))

def delete_image_page(request, imgID):
    #template = loader.get_template('index.html')
    models.Image.objects.all().filter( id=imgID ).delete()
    return HttpResponseRedirect('/')

def delete_image_data(request, imgID):

    try:
        img = models.Image.objects.all().get( id=imgID, uploader_id=request.user.id )
    except models.Image.DoesNotExist:
        messages.add_message(request, messages.INFO, 
            'email does not exists.')
        return HttpResponseRedirect('/image/self')
    except models.Image.MultipleObjectsReturned:
        messages.add_message(request, messages.INFO, 
            'Multiple user found for this email.')
        return HttpResponseRedirect('/image/self')

    img.delete()

    user_db = models.Member.objects.all().get(user=request.user)
    user_db.uploadCount -= 1
    user_db.save()

    return HttpResponseRedirect('/image/self')

def profile_view(request, memberID):
    template = loader.get_template('my_profile.html')
    mem_obj = models.Member.objects.get(id=memberID)

    style_obj = {
        "its_me":False,
        "email":mem_obj.email,
        "description":mem_obj.description,
        "username":mem_obj.username,
    }

    return HttpResponse(template.render(style_obj, request))

def token_generate_new(request):
    email = request.POST.get('email', False)

    if not email:
        return HttpResponse('An Email Address must be supplied')

    token = get_token()

    ti = models.register_Token.objects.create(
        email=email,
        token=token)
    ti.save()

    title = 'ImageX Token'
    content = 'You have been invited to join ImageX. Your Signup Token is:\n{}'.format(token)
    f = sendmail.email_from
    sendmail.send_email(title,content,f,email)

    return HttpResponseRedirect('/token/generate/page')

def token_generate_page(request):
    template = loader.get_template('gen_token.html')
    return HttpResponse(template.render({}, request))

@login_required
def download_image_data(request, imgID):
    # imgID = imgID
    img = models.Image.objects.all().get(id=imgID)
    img_p = os.path.join( settings.MEDIA_ROOT, str(img.imagefile) )

    with open(img_p, 'rb') as fp:
        response = HttpResponse(fp.read())
        file_type, encoding = mimetypes.guess_type(img_p)

        if file_type is None:
            file_type = 'application/octet-stream'

        if encoding is not None:
            response['Content-Encoding'] = encoding

        response['Content-Type'] = file_type
        response['Content-Length'] = str(os.stat(img_p).st_size)

    models.Image.objects.filter(id=imgID).update(download=F('download')+1)
    return response

def password_forget_email(request):
    template = loader.get_template('password_forget_email.html')
    return HttpResponse(template.render({}, request))    

def password_forget_req(request):
    email = request.POST['email']

    try:
        m_db = models.Member.objects.get(email=email)
    except models.Member.DoesNotExist:
        messages.add_message(request, messages.INFO, 
            'email does not exists.')
        return render(request, 'signup.html')
    except models.Member.MultipleObjectsReturned:
        messages.add_message(request, messages.INFO, 
            'Multiple user found for this email.')
        return render(request, 'signup.html')

    passwd_token = get_token()

    ti = models.reset_Token.objects.create(
        email=email,
        token=passwd_token,
        username=m_db.username)
    ti.save()

    title = 'ImageX Password Reset'
    link = 'password/forget/page/{}'.format(passwd_token)
    content = 'Please visit the following link to reset you password:\n{}'.format(link)
    f = sendmail.email_from
    sendmail.send_email(title,content,f,email)

    return HttpResponseRedirect('/signin')

def password_forget_page(request, token):

    t_obj = models.reset_Token.objects.get(token=token)
    u = t_obj.username
    t_obj.delete()

    template = loader.get_template('password_forget_page.html')
    return HttpResponse(template.render({'username':u}, request))

def password_forget_reset(request):
    
    username = request.POST['username']

    if (request.POST['confirm_password'] != request.POST['password']):
        messages.add_message(request, messages.INFO, 
            'Password must be the same!')
        return render(request, 'password_forget_page.html', {'username': username})
    elif (len(request.POST['confirm_password']) == 0 ):
        messages.add_message(request, messages.INFO, 
            'Password cannot be empty')
        return render(request, 'password_forget_page.html', {'username': username})
    
    password = request.POST['password']

    try:
        m_db = models.Member.objects.get(username=username)
    except models.Member.DoesNotExist:
        messages.add_message(request, messages.INFO, 
            'Username does not exist.')
        return render(request, 'signup.html')
    except models.Member.MultipleObjectsReturned:
        messages.add_message(request, messages.INFO, 
            'Multiple users found for this username.')
        return render(request, 'signup.html')

    u = m_db.user
    u.set_password(password)
    u.save()
   
    return HttpResponseRedirect('/signin')

def password_change_page(request):
    template = loader.get_template('password_change.html')
    return HttpResponse(template.render({}, request))

@login_required
def password_change_set(request):
    new_passwd = request.POST['password']
    assert isinstance(new_passwd, str)
    request.user.set_password(new_passwd)
    request.user.save()

    user = authenticate(
        username=request.user.username,
        password=new_passwd)

    login(request, user)

    return HttpResponseRedirect('/')

@login_required
def my_image(request):
    template = loader.get_template('my_image.html')
    images = models.Image.objects.all().filter( uploader_id=request.user.id )
    return HttpResponse(template.render({'images':images,'my_own_pic':True}, request))

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
            p_dict['title'] = ' '.join( p_dict['title'] )
            p_dict['category'] = p_dict['category'][0]
            p_dict['description'] = ' '.join( p_dict['description'])

        except KeyError:
            return redirect( upload_image_page )

        if p_dict['tags'].count(TAG_SEP)>9:
            messages.add_message(request, messages.INFO, 'You can select at most ten tags!')
            return render(request, 'upload_image.html')

        # encode into ,aa,bb,cc, form, for when searching
        # we query ,str, and we can search for the tag
        p_dict['tags'] = TAG_SEP + p_dict['tags'].strip( TAG_SEP ) + TAG_SEP

        user_db = models.Member.objects.get(user=request.user)

        if user_db.uploadCount >= MAX_UPLOAD_TOTAL:
            messages.add_message(request, messages.INFO, 'You have reached your total upload limit!')
            return render(request, 'upload_image.html')

        today = datetime.datetime.now().date()
        if models.Image.objects.filter(
                uploader=request.user.id,
                uploadedOn__gte=today
            ).count() >= MAX_UPLOAD_PER_DAY:
            messages.add_message(request, messages.INFO, 'You have reached your daily upload limit!')
            return render(request, 'upload_image.html')

        print( p_dict['tags'] )

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



@login_required
def update_profile(request):
    update_username = request.POST['username']
    update_email = request.POST['email']
    update_description = request.POST['description']
    
    mem_obj = models.Member.objects.get(user=request.user.id)
    if (len(update_username) != 0):
        models.Member.objects.filter(id=request.user.id).update(username=update_username)
        user = User.objects.get(username = mem_obj.username)
        user.username = update_username
        user.save()
    if (len(update_email) != 0):
        models.Member.objects.filter(id=request.user.id).update(email=update_email)
    models.Member.objects.filter(id=request.user.id).update(description=update_description)
    
    return HttpResponseRedirect('/my_profile')


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

        return HttpResponseRedirect('/')
    else:
        messages.add_message(request, messages.INFO, 'Wrong Username or Password!')
        return render(request, 'signin.html')

def signupdata(request):

    token = request.POST['token']

    try:
        t_obj = models.register_Token.objects.get(token=token)
    except models.register_Token.DoesNotExist:
        messages.add_message(request, messages.INFO, 
            'Token does not exists.')
        return render(request, 'signup.html')
    except models.register_Token.MultipleObjectsReturned:
        messages.add_message(request, messages.INFO, 
            'Multiple emails found for this token.')
        return render(request, 'signup.html')

    email = t_obj.email
    

    if User.objects.filter(username=request.POST['username']).exists():
        messages.add_message(request, messages.INFO, 
            'Too slow! Username has been registered!')
        return render(request, 'signup.html')
    elif (request.POST['confirm_password'] != request.POST['password']):
        messages.add_message(request, messages.INFO, 
            'Password must be the same!')
        return render(request, 'signup.html')
    elif (len(request.POST['confirm_password']) == 0 ):
        messages.add_message(request, messages.INFO, 
            'Password cannot be empty')
        return render(request, 'signup.html')
    elif (len(request.POST['username']) == 0):
        messages.add_message(request, messages.INFO, 
            'Username cannot be empty')
        return render(request, 'signup.html')

    # success scenario
    u = User.objects.create_user(
        username=request.POST['username'], 
        password=request.POST['password'])

    u.save()
    print( 'userId : {}'.format( u.id ) )

    m = models.Member.objects.create(
        user=u,
        email=email,
        username=request.POST['username'])

    m.save()
    t_obj.delete()
    login(request, u)
    return HttpResponseRedirect('/')

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')
