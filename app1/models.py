from django.db import models
from django.contrib.auth.models import User

class Aktyor(models.Model):
    ism = models.CharField(max_length=50)
    davlat = models.CharField(max_length=50)
    tugilgan_yili = models.CharField(max_length=50)
    jins = models.CharField(max_length=50)

    def __str__(self):
        return self.ism



class Kino(models.Model):
    nom = models.CharField(max_length=70)
    janr = models.CharField(max_length=30)
    yil = models.DateField()
    davomiylik = models.DurationField()
    aktyorlar = models.ManyToManyField(Aktyor)
    reyting = models.FloatField()

    def __str__(self):
        return self.nom


class Izoh(models.Model):
    matn = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sana = models.DateField(auto_now_add= True)
    baho = models.PositiveSmallIntegerField()
    kino = models.ForeignKey(Kino,on_delete=models.CASCADE)

    def __str__(self):
        return self.matn

