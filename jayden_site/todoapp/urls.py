from django.urls import path
from . import views

app_name="todo"
urlpatterns=[
        path("",views.MainView.as_view(),name="all"),
    ]