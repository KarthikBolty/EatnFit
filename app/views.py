from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import Meal, BodyWeightEntry
from .forms import MealForm
from .models import DailyGoal

def IndexView(request):
    return render(request, 'app/index.html')


def DashboardView(request):
    today = now().date()
    meals = Meal.objects.filter(created_at=today)

    total_calories = sum(m.calories for m in meals)

    goal_obj = DailyGoal.objects.last()
    daily_goal = goal_obj.goal if goal_obj else 2000

    remaining_calories = max(daily_goal - total_calories, 0)
    progress = (total_calories / daily_goal) * 100 if daily_goal else 0

    context = {
        "total_calories": total_calories,
        "remaining_calories": remaining_calories,
        "progress": round(progress, 2),
        "daily_goal": daily_goal,
        "meals": meals,
    }
    return render(request, "app/dashboard.html", context)


def CalorieView(request):
    today = now().date()
    meals = Meal.objects.filter(created_at=today)
    form = MealForm()

    # ✅ Get latest saved goal or default 2000
    goal_obj = DailyGoal.objects.last()
    daily_goal = goal_obj.goal if goal_obj else 2000

    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("calorie")

    total_calories = sum(m.calories for m in meals)
    remaining_calories = max(daily_goal - total_calories, 0)
    progress = (total_calories / daily_goal) * 100 if daily_goal else 0

    context = {
        "form": form,
        "meals": meals,
        "total_calories": total_calories,
        "daily_goal": daily_goal,
        "remaining_calories": remaining_calories,
        "progress": round(progress, 2),
    }

    return render(request, "app/calorie.html", context)


def delete_meal(request, id):
    Meal.objects.filter(id=id).delete()
    return redirect("calorie")


def BodyweightView(request):
    weights = BodyWeightEntry.objects.all().order_by('-id')

    bmi = None
    status = None

    # ✅ Reset BMI button
    if request.method == "POST" and "reset_bmi" in request.POST:
        return render(request, "app/bodyweight.html", {"weights": weights})

    # ✅ Normal BMI submit
    if request.method == "POST":
        weight = request.POST.get('weight')
        height = request.POST.get('height')

        if weight and height:
            weight = float(weight)
            height_m = float(height) / 100

            bmi = round(weight / (height_m ** 2), 1)

            if bmi < 18.5:
                status = "Underweight"
            elif 18.5 <= bmi < 25:
                status = "Healthy"
            elif 25 <= bmi < 30:
                status = "Overweight"
            else:
                status = "Obese"

            BodyWeightEntry.objects.create(weight=weight)

        return render(request, "app/bodyweight.html", {
            "weights": weights,
            "bmi": bmi,
            "status": status
        })

    return render(request, "app/bodyweight.html", {"weights": weights})

def set_goal(request):
    if request.method == "POST":
        goal = request.POST.get("goal")
        if goal:
            DailyGoal.objects.create(goal=int(goal))
    return redirect("dashboard")


