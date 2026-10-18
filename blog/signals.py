import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Post


@receiver(post_delete, sender=Post)
def delete_cover_image_on_delete(sender, instance, **kwargs):
    """Post delete bhayo bhane image file pani delete garne."""
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            os.remove(instance.cover_image.path)


@receiver(pre_save, sender=Post)
def delete_old_image_on_change(sender, instance, **kwargs):
    """Cover image badaliyo bhane purano file delete garne."""
    if not instance.pk:
        return
    try:
        old = Post.objects.get(pk=instance.pk)
    except Post.DoesNotExist:
        return
    if old.cover_image and old.cover_image != instance.cover_image:
        if os.path.isfile(old.cover_image.path):
            os.remove(old.cover_image.path)