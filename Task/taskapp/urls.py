from django.urls import path
from .views import create_user, update_user, disable_user, assign_role,create_userrole,fetch_user

urlpatterns = [
    path('create/', create_user, name='create_user'),
    path('create1/', create_userrole, name = 'user_role'),
    path('fetch/', fetch_user),
    path('update/<int:pk>/', update_user, name='update_user'),
    path('disable/<int:pk>/', disable_user, name='disable_user'),
    path('role/', assign_role, name='assign_role'),
   
]
