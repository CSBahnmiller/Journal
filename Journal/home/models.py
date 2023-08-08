from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField("Name", max_length=50)
    email = models.EmailField()
    def __str__(self):
        return self.name
