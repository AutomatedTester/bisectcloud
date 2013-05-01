from django.db import models

class TreeInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=200)

class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
