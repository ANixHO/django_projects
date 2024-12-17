from django.shortcuts import render, redirect
from .models import Todo
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django import forms


# Create your views here.

@method_decorator(login_required(login_url='todo:login'), name="dispatch")
class MainView(View):
    def get(self, request):
        todos = Todo.objects.filter(user=self.request.user)
        todos = todos.order_by('completed', 'deadline')
        print(todos)
        username = request.user.username
        context = {"todo_list": todos, "username": username}
        return render(request, "todoapp/todo_list.html", context)


@method_decorator(login_required(login_url='todo:login'), name="dispatch")
class TodoCreateView(CreateView):
    model = Todo
    fields = ["title", "description", "deadline"]
    template_name = "todoapp/new_todo.html"
    success_url = reverse_lazy('todo:all')

    def get_form(self):
        form = super().get_form()
        form.fields["title"].widget.attrs.update({"class": "form-control"})
        form.fields["description"].widget.attrs.update({"class": "form-control"})
        form.fields["deadline"].widget = forms.DateInput(attrs={"type": "date", "class": "form-control"})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required(login_url='todo:login'), name="dispatch")
class TodoUpdateView(UpdateView):
    model = Todo
    fields = ['title', 'description', 'deadline']
    template_name = "todoapp/update_todo.html"
    success_url = reverse_lazy('todo:all')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object();
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)


@login_required(login_url='todo:login')
def check_completed(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    if todo.completed is True:
        todo.completed = False
    else:
        todo.completed = True

    todo.save()
    return redirect("todo:all")


@login_required(login_url='todo:login')
def delete_todo(self, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.delete()
    return redirect("todo:all")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(len(password))

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect("todo:register")

        get_all_user = User.objects.filter(email=email)
        if get_all_user.exists():
            messages.error(request, "Error, Email already registered")
            return redirect("todo:register")

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        login(request, new_user)
        return redirect("todo:all")
    return render(request, "todoapp/register.html", {})


def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        validate_user = authenticate(request, username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect("todo:all")
        else:
            messages.error(request, "Wrong user details, or user does not exist")
            return redirect("todo:login")
    return render(request, "todoapp/login.html", {})
