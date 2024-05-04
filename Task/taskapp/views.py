from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import User
import mailtrap as mt
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer,UserRoleSerializer
from django.utils.crypto import get_random_string



@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fetch_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def disable_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.is_active = False
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def assign_role(request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_userrole(request):
    serializer = UserRoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        elif user is not None and not user.is_active:
            return JsonResponse({'error': 'User account is disabled'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

# def send_login_credentials(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         user = User.objects.get(email=email)
#         if user:
#             password = user.set_random_password() 
#             user.save()
#             send_mail(
#                 'Your login credentials',
#                 f'Your username is: {user.shubham}\nYour password is: {password}',
#                 'shubhamingale1502@gmail.com',
#                 [email],
#                 fail_silently=False,
#             )
#             return JsonResponse({'message': 'Login credentials sent successfully'}, status=200)
#         else:
#             return JsonResponse({'error': 'User not found'}, status=404)

#     return JsonResponse({'error': 'Method not allowed'}, status=405)
@csrf_exempt
def send_login_credentials(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user:
                password = get_random_string(length=12) 
                user.save()
                
                # Send email using Mailtrap
                import mailtrap as mt

                mail = mt.Mail(
                    sender=mt.Address(email="shubhamingale1502@gmail.com", name="Mailtrap Test"),
                    to=[mt.Address(email="sanyogpardeshi@gmail.com")],
                    subject="Your login credentials",
                    text=f"Your username is: {user.username}\nYour password is: {password}",
                    category="Integration Test",
                )

                client = mt.MailtrapClient(token="35a2cafac2ee7c9f14eb569cd8b1bed2")
                client.send(mail)
                
                return JsonResponse({'message': 'Login credentials sent successfully'}, status=200)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

