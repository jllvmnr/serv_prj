from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Book, Category, Author
from .forms import BookForm, CategoryForm, AuthorForm

class BookListView(ListView):
    model = Book
    template_name = 'myapp/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        return Book.objects.filter(is_published=True).select_related('author', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Книги для чтения онлайн'
        context['meta_title'] = 'Книги читать онлайн - Библиотека бесплатных книг'
        context['meta_description'] = 'Читайте книги онлайн бесплатно. Большая коллекция книг различных жанров. Книги, читать которые можно прямо на сайте.'
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'myapp/book_detail.html'
    context_object_name = 'book'
    
    def get_queryset(self):
        return Book.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['meta_title'] = self.object.meta_title
        context['meta_description'] = self.object.meta_description
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'myapp/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'myapp/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.filter(category=self.object, is_published=True)
        context['books'] = books
        context['title'] = f'Книги в категории: {self.object.name}'
        context['meta_title'] = f'{self.object.name} - Книги для чтения'
        context['meta_description'] = f'Читать книги в категории {self.object.name}. {self.object.description}'
        return context

class SearchView(ListView):
    model = Book
    template_name = 'myapp/search_results.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(
                Q(title__icontains=query) | 
                Q(author__name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query),
                is_published=True
            )
        return Book.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query
        context['title'] = f'Результаты поиска: {query}' if query else 'Поиск книг'
        return context

# Admin CRUD Views
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'myapp/admin/book_form.html'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'myapp/admin/book_form.html'
    success_url = reverse_lazy('book_list')

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'myapp/admin/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'myapp/admin/category_form.html'
    success_url = reverse_lazy('category_list')

class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'myapp/admin/author_form.html'
    success_url = reverse_lazy('book_list')