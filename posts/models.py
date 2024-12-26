from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)  # Automatically set to current date and time

    def __str__(self):
        return self.title
class Contestant(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    points = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.surname}'

class Results(models.Model):
    title = models.CharField(max_length=200)  # Title or description of the result
    contestants = models.ManyToManyField(Contestant)  # Link contestants to the result

    def __str__(self):
        return self.title