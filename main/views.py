from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()

    context = {
        "title": "Каталог",
        "products": products
    }

    return render(request, "main/product_list.html", context)

