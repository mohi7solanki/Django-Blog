from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse


def upload_location(instance, filename):
    return f'{instance.slug}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True,
                              width_field="width_field",
                              height_field="height_field",
                              upload_to=upload_location)
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title


def create_slug(instance, new_slug=None):
    slug = slugify(instance)
    if new_slug:
        slug = new_slug
    qs = Post.objects.all().filter(slug=slug).order_by("-id")
    if qs.exists():
        slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
