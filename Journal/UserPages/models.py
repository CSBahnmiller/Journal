from time import localtime, strftime
from django.db import models

# Create your models here.

class User(models.Model):
  fName = models.CharField(max_length=50)
  lName = models.CharField(max_length=50)
  userName = models.CharField(max_length=75)
  password = models.CharField(max_length=100)
  def __str__(self):
    return self.userName
  
class UserContent(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="login")
  mood = models.CharField(max_length=50)
  feeling = models.IntegerField(default=10)
  entryDateTime = models.CharField(max_length=100)
  content = models.TextField()
  def __str__(self):
    return self.feeling
  
  def last_updated(self):
    return(f'Last Updated: {strftime("%a, %d %b %Y %H:%M:%S", localtime())}')