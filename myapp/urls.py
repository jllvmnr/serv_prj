from django.urls import path
from . import views
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BookSitemap, CategorySitemap

sitemaps = {
    "books": BookSitemap,
    "categories": CategorySitemap,
}

urlpatterns = [
    # Public URLs
    path("", BookListView.as_view(), name="book_list"),
    path("books/<slug:slug>/", BookDetailView.as_view(), name="book_detail"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path(
        "categories/<slug:slug>/", CategoryDetailView.as_view(), name="category_detail"
    ),
    path("search/", SearchView.as_view(), name="search"),
    # Admin CRUD 
    path("admin/books/add/", BookCreateView.as_view(), name="book_create"),
    path("admin/books/<slug:slug>/edit/", BookUpdateView.as_view(), name="book_update"),
    path(
        "admin/books/<slug:slug>/delete/", BookDeleteView.as_view(), name="book_delete"
    ),
    path("admin/categories/add/", CategoryCreateView.as_view(), name="category_create"),
    path("admin/authors/add/", AuthorCreateView.as_view(), name="author_create"),
    # Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
