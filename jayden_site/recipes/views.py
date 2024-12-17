from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Recipe


# Create your views here.

class MainView(LoginRequiredMixin, View):
    def get(self, request):
        r = Recipe.objects.all()
        ctx = {'recipes_list': r}
        return render(request, 'recipes/recipes_list.html', ctx)


class OpenView(View):
    def get(self, request):
        return render(request, 'recipes/logout_view.html')
