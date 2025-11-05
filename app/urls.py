from django.urls import path
from .views import IndexView, DashboardView, CalorieView, BodyweightView, delete_meal,set_goal

urlpatterns = [
    path('', IndexView, name='index'),
    path('dashboard/', DashboardView, name='dashboard'),
    path('calorie/', CalorieView, name='calorie'),
    path('delete/<int:id>/', delete_meal, name='delete_meal'),
    path('bodyweight/', BodyweightView, name='bodyweight'),
    path("set-goal/", set_goal, name="set_goal"),

]
