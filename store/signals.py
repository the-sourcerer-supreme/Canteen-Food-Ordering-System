from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    # Customer might be deleted manually; don't crash on user save.
    Customer.objects.get_or_create(user=instance)
