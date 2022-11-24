from distutils.command.upload import upload
from operator import mod
from pyexpat import model
from random import choices
from secrets import choice
from statistics import mode
from tabnanny import verbose
from unicodedata import category
from wsgiref.validate import validator
from django.db import models
from django.contrib.auth.models import User
from .consts import MAX_RATE

RATE_CHOICES = [(x,str(x)) for x in range(0,MAX_RATE+1)]

# Create your models here.
CATEGORY = (('python','python'),('jupyter','jupyter'),('javascript','javascript'))

class Book(models.Model):
    #youser_id = models.IntegerField()
    #user_id = models.ForeignKey(User,on_delete=mpdels.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1500)
    file = models.FileField(upload_to='uploads/',blank=True,null=True,verbose_name='添付ファイル')
    category = models.CharField(
        max_length=50,
        choices=CATEGORY
    )

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #user = models.ForeignKey('auth.User',on_delete=models.CASCADE)

    def __str__(self):
        return self.title