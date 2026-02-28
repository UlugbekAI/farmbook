from django.shortcuts import render

from .models import Category, IrrigationLog, Issue, Product, SprayLog


def home(request):
    context = {
        'issues_count': Issue.objects.count(),
        'protection_count': Product.objects.filter(category__group=Category.CategoryGroup.PROTECTION).count(),
        'fertilizer_count': Product.objects.filter(category__group=Category.CategoryGroup.FERTILIZER).count(),
        'irrigation_count': IrrigationLog.objects.count(),
        'spray_count': SprayLog.objects.count(),
    }
    return render(request, 'core/home.html', context)


def issue_list(request):
    return render(request, 'core/issue_list.html', {'issues': Issue.objects.select_related('crop').all()})


def product_list(request, group):
    products = Product.objects.select_related('category').filter(category__group=group)
    return render(request, 'core/product_list.html', {'products': products, 'group': group})


def irrigation_list(request):
    logs = IrrigationLog.objects.select_related('field', 'crop').all()
    return render(request, 'core/irrigation_list.html', {'logs': logs})


def spray_list(request):
    sprays = SprayLog.objects.select_related('field', 'crop', 'target_issue').prefetch_related('mix_items__product').all()
    return render(request, 'core/spray_list.html', {'sprays': sprays})
