from django.urls import path
from . import views
from rest_framework import routers
from .views import DepartmentViewSet,LoginView
router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet)


urlpatterns = [
    # path('login/', views.login_view, name='login'),
    path('users/', views.UserCreateView.as_view(), name='user-create'),
    path('add_department/', DepartmentViewSet.as_view({'post': 'add_department'}), name='add_department'),
    path('departments/<int:pk>/update/', DepartmentViewSet.as_view({'put': 'update', 'patch': 'update'}), name='departments-update'),
    path('departments/<int:pk>/delete/', DepartmentViewSet.as_view({'delete': 'destroy'}), name='departments-delete'),
    path('login/', LoginView.as_view(), name='login'),

]