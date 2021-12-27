from django.shortcuts import render, redirect
from django.views.generic import View
from LoadScratchProject.forms import ProjectForm


class MainPage(View):
    def get(self, request):
        form = ProjectForm()
        return render(request, "index.html", {'form': ProjectForm()})
