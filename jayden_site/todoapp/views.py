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


# todo list view
# it will only display the todo items that are owned by current login user
# the items are sorted by deadline, less time left todo item will on the top
# completed items will be arranged below in progress 
@method_decorator(login_required(login_url='todo:login'), name="dispatch")
class MainView(View):
    def get(self, request):
        todos = Todo.objects.filter(user=self.request.user)
        todos = todos.order_by('completed', 'deadline')
        username = request.user.username
        context = {"todo_list": todos, "username": username}
        return render(request, "todoapp/todo_list.html", context)


# add new todo view
# it will automatically add the current login user as owner of the todo item
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

# add current user as owner of the todo item
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# update todo view
# user can modify the title, description, and deadline
# the existing content will be automatically filled in the input box
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


# complete status change function
@login_required(login_url='todo:login')
def check_completed(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    if todo.completed is True:
        todo.completed = False
    else:
        todo.completed = True

    todo.save()
    return redirect("todo:all")


# delete todo view
@login_required(login_url='todo:login')
def delete_todo(self, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.delete()
    return redirect("todo:all")


# register view,
# password should at least 8 characters long
# user name should be unique
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect("todo:register")

        get_all_user = User.objects.filter(username=username)
        
        if get_all_user.exists():
            messages.error(request, "Error, user name already registered")
            return redirect("todo:register")

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        login(request, new_user)
        return redirect("todo:all")
    return render(request, "todoapp/register.html", {})


# login view
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
