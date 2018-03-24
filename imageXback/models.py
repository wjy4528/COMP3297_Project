from django import forms
from django.db import models
from django.contrib.auth.models import User

from . import settings

class Image(models.Model):
    download = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=20, default='ABSTRACT')
    title = models.CharField(max_length=30)
    lastModified = models.DateField(auto_now_add=True)
    uploadedOn = models.DateField(auto_now_add=True)
    imagefile = models.FileField()
    tags = models.TextField(null=True)
    uploader = models.ForeignKey(User,on_delete=models.DO_NOTHING)

class Member(models.Model):
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['tags', 'description', 'imagefile', 'uploader', 'category']
