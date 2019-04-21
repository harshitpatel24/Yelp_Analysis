from django.db import models

# Create your models here.

class users(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=2000)

    def __str__(self):
        return self.fname + ' ' + self.lname