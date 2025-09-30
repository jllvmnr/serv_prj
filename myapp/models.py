from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя автора")
    bio = models.TextField(blank=True, verbose_name="Биография")
    photo = models.ImageField(
        upload_to="authors/", blank=True, null=True, verbose_name="Фото"
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    slug = models.SlugField(unique=True, verbose_name="URL")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    description = models.TextField(verbose_name="Описание")
    content = models.TextField(verbose_name="Содержание книги")
    cover_image = models.ImageField(
        upload_to="covers/", blank=True, null=True, verbose_name="Обложка"
    )
    published_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата публикации"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Meta Title")
    meta_description = models.CharField(
        max_length=160, blank=True, verbose_name="Meta Description"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = f"{self.title} - Читать онлайн"
        if not self.meta_description:
            self.meta_description = f"Читать книгу '{self.title}' автора {self.author.name} онлайн. {self.description[:140]}..."
        super().save(*args, **kwargs)
