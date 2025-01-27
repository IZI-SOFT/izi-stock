from django.db import models


class Slides(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Entreprise(models.Model):
    logo = models.ImageField(upload_to='images/')
    texte = models.CharField(max_length=255)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Izisoft(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
