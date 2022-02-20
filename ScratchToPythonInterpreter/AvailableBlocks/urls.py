from django.conf.urls import url
from AvailableBlocks.views import AvailableBlocks

urlpatterns = [
    url(r'AvailableBlocks/', AvailableBlocks.as_view()),
]
