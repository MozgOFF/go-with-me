from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    AuthViewSet,
    MyInfoView,
    MyFollowingView,
    MyFollowersView,
    MyEventsView,
    FollowingEventsView,
    ProfileDetailsView,
    SubscribeView,
    UnSubscribeView,
    ViewedEventsView,
    SavedEventsView,
    UserEventsView,
    FollowingView,
    FollowersView,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('', AuthViewSet, basename='')

appname = 'account'
urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('me', MyInfoView.as_view()),
    path('profile/<int:pk>', ProfileDetailsView.as_view()),
    path('profile/<int:pk>/events', UserEventsView.as_view()),
    path('profile/<int:pk>/following', FollowingView.as_view()),
    path('profile/<int:pk>/followers', FollowersView.as_view()),
    path('profile/<int:pk>/subscribe', SubscribeView.as_view()),
    path('profile/<int:pk>/unsubscribe', UnSubscribeView.as_view()),
    path('detail/<int:pk>', ProfileDetailsView.as_view()),
    path('me/following', MyFollowingView.as_view()),
    path('me/following/events', FollowingEventsView.as_view()),
    path('me/followers', MyFollowersView.as_view()),
    path('me/events', MyEventsView.as_view()),
    path('me/viewed-events', ViewedEventsView.as_view()),
    path('me/saved-events', SavedEventsView.as_view()),
]

urlpatterns += router.urls
