from django.urls import path
from . import views
from .views import TodoCreateView, TodoUpdateView

app_name = "todo"
urlpatterns = [
    path("", views.MainView.as_view(), name="all"),
    path("register/", views.register, name="register"),
    path("login/", views.loginpage, name="login"),
    path("add/", TodoCreateView.as_view(), name="add"),
    path("check_completed/<int:todo_id>", views.check_completed, name="check_completed"),
    path("delete/<int:todo_id>", views.delete_todo, name="delete"),
    path("update/<int:pk>", TodoUpdateView.as_view(), name="update"),
]
