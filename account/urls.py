from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AuthViewSet, MyInfoView, MyFriendsView, FollowersView

router = routers.DefaultRouter(trailing_slash=False)
router.register('', AuthViewSet, basename='')

appname = 'account'
urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('me', MyInfoView.as_view()),
    path('me/following', MyFriendsView.as_view()),
    path('me/followers', FollowersView.as_view()),
]

urlpatterns += router.urls
