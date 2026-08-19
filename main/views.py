from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        "title": "Каталог товарів",
        "categories": categories,
        "category": category,
        "products": products
    }
    return render(request, "main/product_list.html", context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    product.views += 1
    product.save()

    return render(request, 'main/product_detail.html', {"product": product})

