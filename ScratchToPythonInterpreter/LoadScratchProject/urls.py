from django.conf.urls import url
from LoadScratchProject.views.LoadScratchProject import LoadScratchProject
from LoadScratchProject.views.MainPage import MainPage

urlpatterns = [
    url(r'home/', MainPage.as_view()),
    url(r'LoadScratchProject/', LoadScratchProject.as_view()),
]
