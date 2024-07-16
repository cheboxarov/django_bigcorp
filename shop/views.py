from django.shortcuts import render
from .models import ProductProxy, Category, Product


def products_view(request):
    products = ProductProxy.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop/products.html', context)


def product_detail_view(request, slug):
    product = ProductProxy.objects.get(slug=slug)
    context = {
        'product': product
    }
    return render(request, 'shop/product_detail.html', context)


def category_list(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.select_related('category').filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/category_list.html', context)
