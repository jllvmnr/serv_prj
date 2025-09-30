from django.contrib import admin
from .models import Book, Category, Author

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'published_date')
    list_filter = ('is_published', 'category', 'published_date')
    search_fields = ('title', 'author__name', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published_date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)