from django.db import models

from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Слаг для URL")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def get_absolute_url(self):
         return reverse("main:product_list_by_category", args=[self.slug])

    def __str__(self):
            return f"{self.name}"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, db_index=True, verbose_name="Назва продукту")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг для URL")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Зображення")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0, verbose_name="Кількість переглядів")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def get_absolute_url(self):
         return reverse("main:product_detail", args=[self.id, self.slug])

    def __str__(self):
        return f"{self.name} | {self.created_at}"
