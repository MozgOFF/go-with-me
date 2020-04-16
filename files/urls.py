from django.urls import path
from rest_framework.routers import DefaultRouter
from files.views import EventImageUploadView, ImageListView

router = DefaultRouter()
router.register(r'files', EventImageUploadView)

app_name = 'files'
urlpatterns = [
    path('event-image/upload', EventImageUploadView.as_view()),
    path('image/all/', ImageListView.as_view()),
]
