from django.contrib.sitemaps import Sitemap
from .models import Book, Category

class BookSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return Book.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.published_date

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    
    def items(self):
        return Category.objects.all()