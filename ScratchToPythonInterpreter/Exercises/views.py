from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from LoadScratchProject.forms import ProjectForm
import os
import json
from ScratchToPythonInterpreter.settings import BASE_DIR


class Exercises(View):
    def get(self, request):
       # path_to_images = os.getcwd() + '\Exercises\Exercises\\'
       # dirs_in_path = os.listdir(path_to_images)
       # blocks = self.get_images(path_to_images, dirs_in_path)
        with open("Exercises/exercise_manage.json", encoding='utf-8') as f:
            data = json.load(f)

        print(BASE_DIR)
        # print(os.listdir(os.path.join(BASE_DIR, "media\\")))
        # path = os.path.join(BASE_DIR, "media\\") + "Exercises\Exercise1"
        # print(os.listdir(path))
        return render(request, 'Exercises/ExercisesMain.html', {'form': ProjectForm(), 'exercises': data})
        #return render(request, 'Exercises/ExercisesMain.html', {'form': ProjectForm(), 'blocks': blocks})
