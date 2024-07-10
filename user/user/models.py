from django.db import models

class User(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.fname + ' ' + self.lname
