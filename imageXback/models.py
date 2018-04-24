from django import forms
from django.db import models
from django.contrib.auth.models import User
from . import settings

class Image(models.Model):
    download = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    description = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=30, null=True)
    uploadedOn = models.DateTimeField(auto_now_add=True,null=False)
    imagefile = models.FileField()
    tags = models.CharField(max_length=100,null=True)
    uploader = models.ForeignKey(User,on_delete=models.DO_NOTHING)

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, default="null@null", unique=True)
    description = models.CharField(max_length=300, null=True)
    uploadCount = models.IntegerField(default=0)

class ImageForm(forms.ModelForm):
    tags = forms.CharField(required=False)
    category = forms.CharField(required=False)
    description = forms.CharField(required=False)
    title = forms.CharField(required=False)

    class Meta:
        model = Image
        fields = ['tags', 'description','imagefile', 'uploader', 'category','title']

class register_Token(models.Model):
    email = models.EmailField(max_length=50, default="null@null")
    token = models.CharField(max_length=32, primary_key=True)

class reset_Token(models.Model):
    email = models.EmailField(max_length=50, default="null@null")
    token = models.CharField(max_length=32, primary_key=True)
    username = models.CharField(max_length=50)
