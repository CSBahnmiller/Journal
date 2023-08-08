from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserContent(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  mood = models.CharField("Current Mood:", max_length=20, blank=False, choices=[
    ('Happy 😃','Happy 😃'),
    ('Peaceful 😃','Peaceful 😃'),
    ("Sad 😢", "Sad 😢"),
    ("Mad 😤", "Mad 😤"),
    ("Anxious 😰", "Anxious 😰"),
    ("Depressed 😓", "Depressed 😓"),
    ("No Mood 😑","No Mood 😑"),
    ("Angry 😤", "Angry 😤"),
    ("Excited 😃", "Excited 😃"),
    ("Silly 😋", "Silly 😋"),
    ("curious","Curious 🦝"),
    ("Insightful 🤔", "Insightful 🤔"),    
    ], default="Happy 😃")
  feeling = models.IntegerField("On a scale 1-10 how strong is your mood:",blank=False,choices=[tuple([x,x]) for x in range(1,11)], default=10)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  content = models.TextField()

  def __str__(self):
    return self.title + "\n" + self.content