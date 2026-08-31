from django.db.models.fields import related_descriptors
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import request
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import F, Q
from .forms import ContactForm
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def product_list(request, category_slug=None):
    products = Product.objects.select_related('category').filter(is_active=True)
    categories = Category.objects.all()
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    sort = request.GET.get('sort', 'new')

    if sort == 'old':
        products = products.order_by('created_at')
    elif sort == 'popular':
        products = products.order_by('-views', '-created_at')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "title": f"Пошук: {search_query}" if search_query else "Каталог товарів",
        "categories": categories,
        "category": category,
        "products": page_obj,
        "page_obj": page_obj,
        "paginator": paginator,
        "current_sort": sort,
        "search_query": search_query
    }
    return render(request, "main/product_list.html", context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product.objects.select_related('category'), id=id, slug=slug, is_active=True)
    product.views = F('views') + 1
    product.save(update_fields=['views'])
    product.refresh_from_db(fields=['views'])

    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id).select_related('category')[:4]

    context = {
        "title": product.name,
        "product": product,
        "related_products": related_products
    }

    return render(request, 'main/product_detail.html', context)

from django.template.loader import render_to_string

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_text = form.cleaned_data['message']

            email_subject = f"🔔 [NovaStore] Повідомлення від {name}: {subject}"
            
            html_message = render_to_string('main/emails/contact_email.html', {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message_text,
            })
            
            plain_message = f"Ім'я: {name}\nEmail: {email}\nТема: {subject}\n\nПовідомлення:\n{message_text}"
            
            try:
                send_mail(
                    subject=email_subject,
                    message=plain_message,      
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    html_message=html_message,
                    fail_silently=False
                )

                messages.success(request, "Повідомлення успішно відправлене!")
                return redirect('main:contact')
            except Exception as e:
                messages.error(request, f"Помилка при відправленні повідомлення: {e}")

            return redirect('main:contact')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'title': 'Контакти', 'form': form})
