from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count




class Userprofile(models.Model):
    CHOICES = (
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    )
    user = models.ForeignKey(User,related_name='userprofile', on_delete=models.CASCADE,null=True)
    name =models.CharField(max_length=50 ,null=True)
    Sex =models.CharField(max_length=50 ,choices=CHOICES)
    Phone =models.CharField(max_length=50)
    Email =models.EmailField(max_length=200)
    Address = models.CharField(max_length=200 , null=True)
    is_admin = models.BooleanField(blank=True, null=True,default=True)
    def __str__(self):
        return self.name

class Customer(models.Model):
    CHOICES = (
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    )
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200,null=True)
    Phone = models.CharField(max_length=50,null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    Sex =models.CharField(max_length=50 ,choices=CHOICES,null=True)
    Address = models.CharField(max_length=200, null=True,default='El-wiam')
    city = models.CharField(max_length=200, null=True,default='Sidi bel-abbes')
    county = models.CharField(max_length=200, null=True,default='Algérie')
    code = models.CharField(max_length=200, null=True,default='1500')






    def __str__(self):
        return str(self.name)





User.userprofile = property(lambda u:Userprofile.objects.get_or_create(user=u)[0])
User.customer = property(lambda c:Customer.objects.get_or_create(user=c)[0])

