from django.db import models
# Create your models here.

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=False)
    email = models.EmailField(unique=True, null=False)
    passwordHash = models.TextField(null=False)

class Session(models.Model):
    userId = models.IntegerField()
    token = models.TextField(primary_key=True)

class Destination(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    review = models.TextField()
    rating = models.IntegerField()
    public = models.BooleanField()
    userId = models.ForeignKey("User", on_delete=models.CASCADE)