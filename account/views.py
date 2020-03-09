from rest_framework import permissions
from rest_framework import response, decorators, permissions, status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, PasswordChangeSerializer, EmptySerializer

User = get_user_model()

@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    
    refresh = RefreshToken.for_user(user)
    res = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return response.Response(res, status.HTTP_201_CREATED)

class AuthViewSet(viewsets.GenericViewSet):

    serializer_class = EmptySerializer
    serializer_classes = {
        'register': UserCreateSerializer,
        'password_change': PasswordChangeSerializer,
    }

    @decorators.action(methods=['POST'], detail=False, permission_classes=[permissions.AllowAny, ])
    def register(self, request):
        serialier = self.get_serializer(data=request.data)
        serialier.is_valid(raise_exception=True)
        user = serialier.save()
        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return response.Response(res, status.HTTP_201_CREATED)

    @decorators.action(methods=['POST'], detail=False, permission_classes=[permissions.IsAuthenticated, ])
    def password_change(self, request):
        print("asd", request.data)

        serializer = self.get_serializer(data=request.data)      

        if not serializer.is_valid():
            return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        print("serializer validated_data", serializer.validated_data['current_password'])
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
