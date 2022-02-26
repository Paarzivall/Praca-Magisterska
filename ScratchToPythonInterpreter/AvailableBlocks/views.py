from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from LoadScratchProject.forms import ProjectForm
import os


class AvailableBlocks(View):
    def get(self, request):
        path_to_images = os.getcwd() + '\AvailableBlocks\ScratchBlocks\\'
        dirs_in_path = os.listdir(path_to_images)
        blocks = self.get_images(path_to_images, dirs_in_path)
        # print(type(blocks))
        return render(request, 'AvailableBlocks/AvailableBlocksMain.html', {'form': ProjectForm(), 'blocks': blocks})

    def get_images(self, path_to_images, dirs):
        list_of_all_files = list()
        for dir in dirs:
            if len(os.listdir(path_to_images + dir)) > 0:
                list_of_files = list()
                path = path_to_images + dir
                for block in os.listdir(path):
                    # print('img/ScratchBlocks/' + dir + '/' + block)
                    list_of_files.append({'path': 'ScratchBlocks/' + dir + '/' + block, 'alt': block[:len(block) - 4]})
                list_of_all_files.append({'type_of_blocks': dir, 'files': list_of_files})
            #else:
            #    dict_of_all_files[dir] = None
        return list_of_all_files

