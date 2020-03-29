from django.urls import path
from event.views import EventCreateView, EventListView, EventDetailView, EventCommentsView

app_name = 'event'
urlpatterns = [
    path('create/', EventCreateView.as_view()),
    path('all/', EventListView.as_view()),
    path('detail/<int:pk>/', EventDetailView.as_view()),
    path('detail/<int:pk>/comments/', EventCommentsView.as_view()),
    # path('detail/<int:pk>/Update', EventDetailView.as_view()),
    # path('detail/<int:pk>/', EventDetailView.as_view()),
]
