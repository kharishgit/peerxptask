from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework import generics,status
from support.models import User
from .serializers import UserSerializer,LoginSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


# class LoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })
def login_view(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        user = authenticate(request, email_or_phone=email_or_phone, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Successfully logged in")

            return redirect('UserCreateView')
        else:
            # Handle invalid login
            return HttpResponse("Invalid username or password")
    else:
        return render(request, 'login.html')


class UserCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()