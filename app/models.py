from django.db import models

class CalorieEntry(models.Model):
    food_name = models.CharField(max_length=100)
    calories = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} - {self.calories} cal"


class BodyWeightEntry(models.Model):
    weight = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.weight} kg on {self.date}"
    
class QuickFood(models.Model):
    """
    Optional helper table for quick-select foods.
    You can pre-populate some common foods via admin.
    """
    name = models.CharField(max_length=150)
    calories = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.calories} cal)"


from django.db import models

class Meal(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    food_name = models.CharField(max_length=200)
    calories = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} ({self.calories} cal)"


class BodyWeightEntry(models.Model):
    weight = models.FloatField()
    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.weight} kg"
    
class DailyGoal(models.Model):
    goal = models.IntegerField(default=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.goal} kcal"

