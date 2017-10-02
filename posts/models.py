from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from tinymce import HTMLField
from mptt.models import MPTTModel, TreeForeignKey


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


# def upload_location(instance, filename):
#     return f'{instance.slug}/{filename}'

def upload_location(instance, filename):
    return '{}/{}'.format(instance.slug, filename)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=150)
    category = models.ForeignKey('Category', null=True, blank=True)
    content = HTMLField('Content')
    image = models.ImageField(null=True, blank=True,
                              width_field="width_field",
                              height_field="height_field",
                              upload_to=upload_location)
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    slug = models.SlugField(unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    objects = PostManager()

    def __str__(self):
        return self.title

    def get_slug_list_for_categories(self):
        try:
            ancestors = self.category.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))

        return slugs

    class Meta:
        ordering = ["-timestamp", "-updated"]


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'

    def get_slug_list_for_categories(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))

        return slugs

    def __str__(self):
        return self.name


# noinspection PyPackageRequirements
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
