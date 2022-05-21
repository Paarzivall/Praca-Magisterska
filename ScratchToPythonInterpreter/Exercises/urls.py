from django.conf.urls import url
from Exercises.views import Exercises

urlpatterns = [
    url(r'Exercises/', Exercises.as_view()),
]
