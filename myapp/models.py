from django.db import models

# Create your models here.


class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)


class User(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.BigIntegerField()
    image = models.CharField(max_length=500)
    wallet_address = models.CharField(max_length=500)


class SchemeCategory(models.Model):
    name=models.CharField(max_length=100)


class Complaint(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    complaint=models.CharField(max_length=500)
    status=models.CharField(max_length=100,default='pending')
    reply=models.CharField(max_length=100,default='pending')


class RequestStatus(models.Model):
    SCHEMEREQUEST=models.IntegerField()
    Amount=models.FloatField(default=0)
    Status=models.CharField(max_length=100)

class Transactions(models.Model):
    SCHEMEREQUEST=models.IntegerField()
    Date=models.DateField()
    Amount=models.FloatField()
    Status=models.CharField(max_length=100)
    Sender=models.CharField(max_length=100)
    Reciever=models.CharField(max_length=100)

