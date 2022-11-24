from distutils.command.upload import upload
from operator import mod
import profile
from pyexpat import model
from random import choices
from secrets import choice
from statistics import mode
from tabnanny import verbose
from unicodedata import category
from wsgiref.validate import validator
from django.db import models
from django.contrib.auth.models import User
from book.models import Book,Review

# Create your models here.
class User_Home(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    text = models.TextField(max_length=300,blank=True,null=True)
    thumbnail = models.ImageField(blank=True,null=True)
    #book = models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.username
