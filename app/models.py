from django.db import models
from django.contrib.auth.models import User

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    food_name = models.CharField(max_length=100)
    calories = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} ({self.calories} cal)"


class BodyWeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    weight = models.FloatField()
    height = models.FloatField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.weight} kg on {self.created_at}"



class QuickFood(models.Model):
    name = models.CharField(max_length=150)
    calories = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.calories} cal)"


class DailyGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goal = models.IntegerField(default=2000)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

