from django.urls import path
from .views import *

# app/urls.py

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("calorie/", CalorieView.as_view(), name="calorie"),
    path("meal/delete/<int:id>/", DeleteMealView.as_view(), name="delete_meal"),
    path("bodyweight/", BodyweightView.as_view(), name="bodyweight"),
    path("set-goal/", SetGoalView.as_view(), name="set_goal"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/meals/summary/today/", DailySummaryAPIView.as_view(), name="daily-summary-api"),

]




