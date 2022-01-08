from django.shortcuts import render, redirect
from django.views.generic import View
from scratchclient import ScratchSession, Project
from LoadScratchProject.forms import ProjectForm
from LoadScratchProject.views.Converter.DrawAsScratchCode import DrawAsScratchCode
from LoadScratchProject.views.Converter.DrawAsPythonCode import DrawAsPythonCode
from LoadScratchProject.views.Converter.PriorityListOfElements import PriorityListOfElements
from LoadScratchProject.views.Converter.Files import Files


class LoadScratchProject(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                file = Files(request.FILES.get('project'))
                priority_list = PriorityListOfElements(file.get_json_file())
                scratch_code = DrawAsScratchCode(priority_list.get_priority_list()).get_scratch_code()
                python_code = DrawAsPythonCode(priority_list.get_priority_list()).get_python_code()
                results = file.get_json_file()
        return render(request, "index.html", {'form': ProjectForm(), 'python_code_result': python_code,
                                              'scratch_code_result': scratch_code})
    """def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                id = form['project_id'].value()
                session = ScratchSession("test_mgr123", "test_mgr123@")
                autor = session.get_project(id).author.username
                tytul = session.get_project(id).title
                results = session.get_project(id).get_scripts()  # 585648438
                Converter(id)
                return render(request, "index.html", {'form': form, 'autor': autor, 'tytul': tytul,
                                                      'python_code_result': results, 'scratch_code_result': results})
        else:
            return render(request, "index.html", {'form': ProjectForm()})"""
