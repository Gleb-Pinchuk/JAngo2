from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.core.cache import cache
from .models import Product, Category
from .services import get_products_by_category


class HomeView(ListView):
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        cache_key = 'published_products'
        products = cache.get(cache_key)
        if products is None:
            products = list(Product.objects.filter(is_published=True))
            cache.set(cache_key, products, timeout=60 * 15)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


@method_decorator(cache_page(60 * 15), name='dispatch')
@method_decorator(vary_on_headers('Cookie'), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        # Очистка кеша после создания
        cache.delete('published_products')
        if self.object.category_id:
            cache.delete(f'products_by_category_{self.object.category_id}')
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого товара.")
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        # Очистка кеша после обновления
        cache.delete('published_products')
        cache.delete(f'products_by_category_{self.object.category_id}')
        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner == self.request.user or self.request.user.has_perm('catalog.delete_product'):
            return obj
        raise PermissionDenied("У вас нет прав на удаление этого товара.")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        category_id = obj.category_id
        response = super().delete(request, *args, **kwargs)
        cache.delete('published_products')
        cache.delete(f'products_by_category_{category_id}')
        return response


class UnpublishProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        old_category_id = product.category_id
        product.is_published = False
        product.save()
        cache.delete('published_products')
        cache.delete(f'products_by_category_{old_category_id}')
        messages.success(request, f'Товар "{product.name}" снят с публикации.')
        return redirect('product_detail', pk=pk)


class ProductsByCategoryView(ListView):
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'


    def get_queryset(self):
        category_id = self.kwargs['category_id']
        cache_key = f'products_by_category_{category_id}'
        products = cache.get(cache_key)
        if products is None:
            products = list(get_products_by_category(category_id))
            cache.set(cache_key, products, timeout=60 * 15)
        return products


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, id=self.kwargs['category_id'])
        return context
