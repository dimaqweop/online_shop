from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Користувач')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Біографія')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Аватар')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата народження')
    location = models.CharField(max_length=50, blank=True, verbose_name='Місцезнаходження')
    website = models.URLField(max_length=200, blank=True, verbose_name='Веб-сайт')

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'

    def __str__(self):
        return f'{self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)

    
    
