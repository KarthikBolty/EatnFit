# app/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import localdate
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Meal, BodyWeightEntry, DailyGoal
from .forms import MealForm

# Small built-in quick food list to use instead of an external API
QUICK_FOODS = [
    {"name": "Apple", "cal": 95},
    {"name": "Banana", "cal": 105},
    {"name": "Chicken Breast 100g", "cal": 165},
    {"name": "Brown Rice 100g", "cal": 111},
    {"name": "Salmon 100g", "cal": 208},
    {"name": "Greek Yogurt", "cal": 100},
    {"name": "Oatmeal 100g", "cal": 68},
    {"name": "Avocado", "cal": 160},
    {"name": "2 Eggs", "cal": 155},
    {"name": "Sweet Potato 100g", "cal": 86},
]

# ------- Simple index -------
class IndexView(TemplateView):
    template_name = "app/index.html"


# ------- Dashboard -------
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "app/dashboard.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localdate()

        goal_obj, _ = DailyGoal.objects.get_or_create(user=self.request.user)
        daily_goal = goal_obj.goal

        meals = Meal.objects.filter(user=self.request.user, created_at=today)
        total_calories = sum(meal.calories for meal in meals)
        remaining_calories = max(daily_goal - total_calories, 0)
        progress = (total_calories / daily_goal * 100) if daily_goal else 0

        context.update({
            "total_calories": total_calories,
            "remaining_calories": remaining_calories,
            "progress": round(progress, 2),
            "daily_goal": daily_goal,
        })
        return context


# ------- Calorie page (show + add meal) -------
class CalorieView(LoginRequiredMixin, FormView):
    template_name = "app/calorie.html"
    form_class = MealForm
    success_url = reverse_lazy("calorie")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        meal = form.save(commit=False)
        meal.user = self.request.user
        meal.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localdate()
        goal_obj, _ = DailyGoal.objects.get_or_create(user=self.request.user)
        daily_goal = goal_obj.goal
        meals = Meal.objects.filter(user=self.request.user, created_at=today)
        total_calories = sum(meal.calories for meal in meals)
        remaining_calories = max(daily_goal - total_calories, 0)
        progress = (total_calories / daily_goal * 100) if daily_goal else 0

        context.update({
            "meals": meals,
            "total_calories": total_calories,
            "remaining_calories": remaining_calories,
            "progress": progress,
            "daily_goal": daily_goal,
            # provide quick foods for template autofill
            "quick_foods": QUICK_FOODS,
        })
        return context


# ------- Delete meal -------
class DeleteMealView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request, id):
        Meal.objects.filter(id=id, user=request.user).delete()
        return redirect("calorie")

    def get(self, request, id):
        return redirect("calorie")


# ------- Bodyweight & BMI -------
class BodyweightView(LoginRequiredMixin, TemplateView):
    template_name = "app/bodyweight.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weights = BodyWeightEntry.objects.filter(user=self.request.user).order_by('-id')
        context["weights"] = weights
        return context

    def post(self, request, *args, **kwargs):
        weights = BodyWeightEntry.objects.filter(user=request.user).order_by('-id')

        if "reset_bmi" in request.POST:
            return render(request, self.template_name, {"weights": weights})

        weight = request.POST.get('weight')
        height = request.POST.get('height')
        bmi = None
        status = None

        if weight and height:
            try:
                weight_f = float(weight)
                height_m = float(height) / 100.0
                BodyWeightEntry.objects.create(user=request.user, weight=weight_f, height=height)
                bmi = round(weight_f / (height_m ** 2), 1)
                if bmi < 18.5:
                    status = "Underweight"
                elif 18.5 <= bmi < 25:
                    status = "Healthy"
                elif 25 <= bmi < 30:
                    status = "Overweight"
                else:
                    status = "Obese"
            except (ValueError, ZeroDivisionError):
                messages.error(request, "Invalid height/weight values")

        return render(request, self.template_name, {
            "weights": weights,
            "bmi": bmi,
            "status": status
        })


# ------- Set daily goal -------
class SetGoalView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        goal = request.POST.get("goal")
        if goal:
            try:
                DailyGoal.objects.update_or_create(
                    user=request.user,
                    defaults={"goal": int(goal)}
                )
            except ValueError:
                messages.error(request, "Invalid goal value")
        return redirect("dashboard")


# ------- Register -------
class RegisterView(FormView):
    template_name = "app/register.html"
    success_url = reverse_lazy("dashboard")

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# ------- Login -------
class LoginView(FormView):
    template_name = "app/login.html"
    success_url = reverse_lazy("dashboard")

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(self.success_url)
        else:
            messages.error(request, "Invalid credentials")
            return render(request, self.template_name)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# ------- Logout -------
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
    

class DailySummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = localdate()

        meals = Meal.objects.filter(
            user=request.user,
            created_at=today
        )

        total_calories = meals.aggregate(
            total=Sum('calories')
        )['total'] or 0

        meal_count = meals.count()

        goal_obj, _ = DailyGoal.objects.get_or_create(user=request.user)
        daily_goal = goal_obj.goal

        return Response({
            "date": today,
            "total_calories": total_calories,
            "meal_count": meal_count,
            "goal": daily_goal,
            "remaining_calories": max(daily_goal - total_calories, 0)
        })


   
