import calendar
import io
import logging
import os
import statistics
from collections import Counter
from decimal import Decimal

import requests
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, F, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PartForm, RegistrationForm, ReviewForm, SaleForm
from .models import (
    Client,
    CompanyInfo,
    Employee,
    NewsArticle,
    Part,
    ProductType,
    PromoCode,
    Review,
    Sale,
    Supplier,
    Term,
    Vacancy,
)

logger = logging.getLogger(__name__)


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_authenticated and (user.is_staff or user.is_superuser))(view_func)


def _calendar_text():
    today = timezone.localdate()
    return calendar.month(today.year, today.month)


def _base_time_context():
    now_utc = timezone.now()
    return {
        'now_utc': now_utc,
        'now_local': timezone.localtime(now_utc),
        'server_timezone': timezone.get_current_timezone_name(),
        'text_calendar': _calendar_text(),
    }


def _safe_api_get(url, fallback, timeout=2):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logger.warning('External API failed: %s', exc)
        return fallback


def home(request):
    latest_news = NewsArticle.objects.filter(is_published=True).first()
    context = {
        'latest_news': latest_news,
        'parts_count': Part.objects.filter(is_active=True).count(),
        'suppliers_count': Supplier.objects.count(),
        'active_promos': PromoCode.objects.filter(is_active=True).count(),
    }
    context.update(_base_time_context())
    return render(request, 'shop/home.html', context)


def about(request):
    return render(request, 'shop/about.html', {'items': CompanyInfo.objects.all(), **_base_time_context()})


def news_list(request):
    return render(
        request,
        'shop/news_list.html',
        {'articles': NewsArticle.objects.filter(is_published=True), **_base_time_context()},
    )


def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)
    return render(request, 'shop/news_detail.html', {'article': article, **_base_time_context()})


def terms(request):
    return render(request, 'shop/terms.html', {'terms': Term.objects.all(), **_base_time_context()})


def contacts(request):
    return render(request, 'shop/contacts.html', {'employees': Employee.objects.all(), **_base_time_context()})


def privacy(request):
    return render(request, 'shop/privacy.html', _base_time_context())


def vacancies(request):
    return render(request, 'shop/vacancies.html', {'vacancies': Vacancy.objects.all(), **_base_time_context()})


def reviews(request):
    return render(
        request,
        'shop/reviews.html',
        {'reviews': Review.objects.filter(is_approved=True), **_base_time_context()},
    )


@login_required
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.name = request.user.get_full_name() or request.user.username
            review.save()
            messages.success(request, 'Отзыв сохранен.')
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'shop/form.html', {'form': form, 'title': 'Добавить отзыв', **_base_time_context()})


def promos(request):
    return render(request, 'shop/promos.html', {'promos': PromoCode.objects.all(), **_base_time_context()})


def part_list(request):
    parts = Part.objects.select_related('product_type', 'manufacturer').filter(is_active=True)
    return render(
        request,
        'shop/part_list.html',
        {'parts': parts, 'types': ProductType.objects.all(), **_base_time_context()},
    )


def part_detail(request, pk):
    part = get_object_or_404(
        Part.objects.select_related('product_type', 'manufacturer').prefetch_related('suppliers'),
        pk=pk,
    )
    return render(request, 'shop/part_detail.html', {'part': part, **_base_time_context()})


@staff_required
def part_create(request):
    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, 'Товар добавлен.')
            return redirect(part)
    else:
        form = PartForm()
    return render(request, 'shop/form.html', {'form': form, 'title': 'Новый товар', **_base_time_context()})


@staff_required
def part_update(request, pk):
    part = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар обновлен.')
            return redirect(part)
    else:
        form = PartForm(instance=part)
    return render(request, 'shop/form.html', {'form': form, 'title': 'Редактировать товар', **_base_time_context()})


@staff_required
def part_delete(request, pk):
    part = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        part.is_active = False
        part.save(update_fields=['is_active', 'updated_at_utc', 'updated_at_local_text'])
        messages.success(request, 'Товар удален.')
        return redirect('part_list')
    return render(request, 'shop/confirm_delete.html', {'object': part, 'title': 'Удалить товар', **_base_time_context()})


@login_required
def sale_create(request):
    client = getattr(request.user, 'client_profile', None)
    if not client:
        messages.error(request, 'Для покупки нужен профиль клиента.')
        return redirect('profile')
    if request.method == 'POST':
        form = SaleForm(request.POST, client=client)
        if form.is_valid():
            sale = form.save()
            messages.success(request, f'Покупка сохранена: {sale.part.name}.')
            return redirect('profile')
    else:
        initial = {'part': request.GET.get('part')} if request.GET.get('part') else None
        form = SaleForm(client=client, initial=initial)
    return render(request, 'shop/form.html', {'form': form, 'title': 'Купить товар', **_base_time_context()})


@login_required
def profile(request):
    client = getattr(request.user, 'client_profile', None)
    employee = getattr(request.user, 'employee_profile', None)
    sales = Sale.objects.select_related('part').filter(client=client) if client else Sale.objects.none()
    staff_sales = Sale.objects.select_related('client', 'part').all()[:20] if request.user.is_staff else []
    return render(
        request,
        'shop/profile.html',
        {'client': client, 'employee': employee, 'sales': sales, 'staff_sales': staff_sales, **_base_time_context()},
    )


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация завершена.')
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'shop/registration/register.html', {'form': form, **_base_time_context()})


def external_apis(request):
    cat_fact = _safe_api_get('https://catfact.ninja/fact', {'fact': 'API временно недоступен.'})
    ip_info = _safe_api_get('https://api.ipify.org?format=json', {'ip': 'не удалось получить'})
    return render(
        request,
        'shop/external_apis.html',
        {'cat_fact': cat_fact.get('fact'), 'ip': ip_info.get('ip'), **_base_time_context()},
    )


@login_required
def parts_api(request):
    parts = Part.objects.filter(is_active=True).values('sku', 'name', 'price', 'quantity')
    return JsonResponse({'results': list(parts)})


@login_required
def stats(request):
    sales = Sale.objects.select_related('part', 'part__product_type')
    totals = [sale.total_price for sale in sales]
    type_counter = Counter(sale.part.product_type.name for sale in sales)
    total_sum = sum(totals, Decimal('0.00'))
    stat_values = {
        'total_sum': total_sum,
        'average': statistics.mean(totals) if totals else Decimal('0.00'),
        'median': statistics.median(totals) if totals else Decimal('0.00'),
        'mode': statistics.mode(totals) if totals else Decimal('0.00'),
        'top_type': type_counter.most_common(1)[0][0] if type_counter else 'нет данных',
    }
    parts_by_name = Part.objects.order_by('name')
    return render(
        request,
        'shop/stats.html',
        {'stat_values': stat_values, 'parts_by_name': parts_by_name, **_base_time_context()},
    )


@login_required
def sales_chart(request):
    os.environ.setdefault('MPLCONFIGDIR', os.path.join(os.getcwd(), '.matplotlib'))
    import matplotlib

    matplotlib.use('Agg')
    from matplotlib import pyplot as plt

    data = (
        Sale.objects.values(type_name=F('part__product_type__name'))
        .annotate(total=Sum(F('quantity') * F('unit_price')), count=Count('id'))
        .order_by('type_name')
    )
    labels = [row['type_name'] for row in data]
    values = [float(row['total'] or 0) for row in data]
    if not labels:
        labels = ['Нет продаж']
        values = [0]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color='#2f6f73')
    ax.set_title('Выручка по типам товаров')
    ax.set_ylabel('BYN')
    ax.tick_params(axis='x', rotation=25)
    fig.tight_layout()
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')

# Create your views here.
