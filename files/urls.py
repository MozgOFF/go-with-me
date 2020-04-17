from django.urls import path
from files.views import EventImageUploadView, EventImageListView, UserImageUploadView

app_name = 'files'
urlpatterns = [
    path('event-image/upload', EventImageUploadView.as_view()),
    path('user-image/upload', UserImageUploadView.as_view()),
    path('event-image/all/', EventImageListView.as_view()),
]
