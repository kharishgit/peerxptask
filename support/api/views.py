from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework import generics,status,viewsets,views
from support.models import User,Department
from .serializers import UserSerializer,LoginSerializer,DepartmentSerializer
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action


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

        print(email_or_phone,password)

        user = authenticate(request, email_or_phone=email_or_phone, password=password)
        print('hii',user)
        if user is not None:
            login(request, user)
            return HttpResponse("Successfully logged in")

            # return redirect('UserCreateView')
        else:
            # Handle invalid login
            return HttpResponse("Invalid username or password")
    else:
        return render(request, 'login.html')


class UserCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    @action(methods=['post'], detail=False)
    def add_department(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

#START
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAdminUser,)
#END

class LoginView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email_or_phone = request.data.get("email_or_phone")
        password = request.data.get("password")
        user = authenticate(request, email_or_phone=email_or_phone, password=password)
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)