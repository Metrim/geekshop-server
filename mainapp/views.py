from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView

# Create your views here.

from mainapp.models import Product, ProductCategory


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page=1):
    context = {
        'title': 'GeekShop - Каталог',
        'categories': ProductCategory.objects.all(),
    }
    # Делаем через тернарный оператор:
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context.update({'products': products_paginator})
    # if category_id:
    #     products = Product.objects.filter(category_id=category_id)
    #     # context.update({'products': products})  # Аналогично: context['products'] = products
    # else:
    #     products =Product.objects.all()
    # context = {
    #     'title': 'GeekShop - Каталог',
    #     'products': Product.objects.all(),
    #     # 'products': [
    #     #     {'name': 'Худи черного цвета с монограммами adidas Originals',
    #     #      'price': 6090.00,
    #     #      'src': 'Adidas-hoodie.png',
    #     #      'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.', },
    #     #     {'name': 'Синяя куртка The North Face',
    #     #      'price': 23725.00,
    #     #      'src': 'Blue-jacket-The-North-Face.png',
    #     #      'description': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.', },
    #     #     {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
    #     #      'price': 3390.00,
    #     #      'src': 'Brown-sports-oversized-top-ASOS-DESIGN.png',
    #     #      'description': 'Материал с плюшевой текстурой. Удобный и мягкий.', },
    #     #     {'name': 'Черный рюкзак Nike Heritage',
    #     #      'price': 2340.00,
    #     #      'src': 'Black-Nike-Heritage-backpack.png',
    #     #      'description': 'Плотная ткань. Легкий материал.', },
    #     #     {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
    #     #      'price': 13590.00,
    #     #      'src': 'Black-Dr-Martens-shoes.png',
    #     #      'description': 'Гладкий кожаный верх. Натуральный материал.', },
    #     #     {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
    #     #      'price': 2890.00,
    #     #      'src': 'Dark-blue-wide-leg-ASOs-DESIGN-trousers.png',
    #     #      'description': 'Легкая эластичная ткань сирсакер Фактурная ткань.', },
    #     # ]
    #     'categories': ProductCategory.objects.all(),
    # }
    return render(request, 'mainapp/products.html', context)

