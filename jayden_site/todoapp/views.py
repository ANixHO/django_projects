from django.shortcuts import render
from .models import Todo
from django.views.generic import View

# Create your views here.

class MainView(View):
    def get(self, request):
        todos=Todo.objects.all()
        context={"todo_list":todos}

        return render(request, "todoapp/todo_list.html",context)

