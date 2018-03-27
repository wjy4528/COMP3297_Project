from django import forms
from django.db import models
from django.contrib.auth.models import User

from . import settings

class Image(models.Model):
    download = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=20, default='abstract')
    title = models.CharField(max_length=30)
    lastModified = models.DateField(auto_now_add=True)
    uploadedOn = models.DateField(auto_now_add=True)
    imagefile = models.FileField()
    tags = models.TextField(null=True)
    uploader = models.ForeignKey(User,on_delete=models.DO_NOTHING)

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, default="null@null")
    description = models.CharField(max_length=300, null=True)
    uploadCount = models.IntegerField(default=0)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['tags', 'description', 'imagefile', 'uploader', 'category']
