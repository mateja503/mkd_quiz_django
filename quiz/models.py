from django.db import models

from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('Science', 'Science'),
        ('History', 'History'),
        ('General', 'General Knowledge'),
        ('Art', 'Art'),
        ('Sport', 'Sport'),
    ]
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    question_text = models.CharField(max_length=255)
    choice_1 = models.CharField(max_length=255)
    choice_2 = models.CharField(max_length=255)
    choice_3 = models.CharField(max_length=255)
    choice_4 = models.CharField(max_length=255)
    correct_choice = models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return f"{self.question_text} ({self.category}, {self.difficulty})"

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.score}'