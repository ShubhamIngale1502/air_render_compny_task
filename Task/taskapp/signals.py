from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import User, UserRole, UserLog



@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='LOGIN')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='LOGOUT')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='LOGIN')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='LOGOUT')

@receiver(post_save, sender=UserRole)
def log_user_role_change(sender, instance, created, **kwargs):
    if created:
        action = 'ASSIGNED ROLE'
    else:
        action = 'UPDATED ROLE'
    UserLog.objects.create(user=instance.user, action=action, role=instance.role)