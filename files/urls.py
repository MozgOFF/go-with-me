from django.urls import path
from rest_framework.routers import DefaultRouter
from files.views import ImageViewSet, ImageListView

router = DefaultRouter()
router.register(r'files', ImageViewSet)

app_name = 'files'
urlpatterns = [
    path('image/upload/', ImageViewSet.as_view()),
    path('image/all/', ImageListView.as_view()),
]
