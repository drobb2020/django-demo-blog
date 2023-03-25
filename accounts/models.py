from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_directory_path, default='users/avatar.jpg')
    bio = RichTextField()
    favorite_quote = RichTextField()

    def clean(self):
        if not self.avatar:
            raise ValidationError('x')
        else:
            w, h = get_image_dimensions(self.avatar)
            if w >= 250:
                raise ValidationError('x')
            if h >= 250:
                raise ValidationError('x')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
