import random
from django.db import models
from django.utils.text import slugify
import string
from django.urls import reverse


def rand_slug():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class Category(models.Model):
    name = models.CharField(verbose_name="Категория", max_length=100, db_index=True)
    parent_category = models.ForeignKey('self', verbose_name='Родитель', null=True, blank=True,
                                        related_name='children', on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        unique_together = (('parent_category', 'slug'),)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.name]
        k = self.parent_category
        while k is not None:
            full_path.append(k.name)
            k = k.parent_category
        return ' > '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + '-' + self.name)
        super(Category, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('shop:category', kwargs={'slug': self.slug})


class Product(models.Model):
    title = models.CharField('Название', max_length=250, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField('Бренд', max_length=100, db_index=True)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField(verbose_name='URL', max_length=250, unique=True, null=False, editable=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, default=99.99)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('shop:product', kwargs={'slug': self.slug})


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy = True
