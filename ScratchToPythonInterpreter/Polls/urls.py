from django.conf.urls import url
from LoadScratchProject.views.LoadScratchProject import LoadScratchProject
from Polls.views.PollsMainPage import PollsMainPage
from Polls.views.PollsReceiver import PollsReceiver

urlpatterns = [
    url(r'polls/', PollsMainPage.as_view()),
    url(r'pollsSend/', PollsReceiver.as_view()),
]
