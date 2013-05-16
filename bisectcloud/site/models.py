from django.db import models

class TreeInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=200)

class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class TaskMaster(models.Model):
    id = models.AutoField(primary_key=True)
    bad = models.CharField(max_length=50)
    good = models.CharField(max_length=50)
    test = models.CharField(max_length=255)
    cancelled = models.BooleanField()
    platform = models.ForeignKey(Platform)
    tree = models.ForeignKey(TreeInfo)

