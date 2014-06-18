#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Categorie(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=45, unique=True, db_column='name')
    description = models.TextField(db_column='description')
    class Meta:
        db_table = 'Categories'
    def __str__(self):
        return self.name

class Challenge(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=45, unique=True, db_column='name')
    img = models.CharField(max_length=255, unique=False, db_column='img')
    description = models.TextField(db_column='description')
    points = models.IntegerField(null=False, blank=False, db_column='points')
    url = models.CharField(max_length=255, unique=True, db_column='url')
    flag = models.CharField(max_length=255, unique=True, db_column='flag')
    categorie = models.ForeignKey('Categorie', to_field='id', blank=True, null=True, on_delete=models.SET_NULL, db_column='categorie')
    seuil = models.IntegerField(default=0, null=False, blank=False, db_column='seuil')
    private = models.BooleanField(default=True, db_column='blocked')
    class Meta:
        db_table = 'Challenges'
    def __str__(self):
        return self.name

class Validation(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user = models.ForeignKey(User) 
    chall = models.ForeignKey('Challenge', to_field='id', db_column='chall')
    value = models.IntegerField(null=False, blank=False, db_column='value')
    timestamp = models.DateTimeField(default=lambda :datetime.now(), db_column='timestamp')
    class Meta:
        db_table = 'Validations'
