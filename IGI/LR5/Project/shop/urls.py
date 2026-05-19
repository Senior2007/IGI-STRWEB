from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^news/$', views.news_list, name='news_list'),
    re_path(r'^news/(?P<slug>[-\w]+)/$', views.news_detail, name='news_detail'),
    re_path(r'^terms/$', views.terms, name='terms'),
    re_path(r'^contacts/$', views.contacts, name='contacts'),
    re_path(r'^privacy/$', views.privacy, name='privacy'),
    re_path(r'^vacancies/$', views.vacancies, name='vacancies'),
    re_path(r'^reviews/$', views.reviews, name='reviews'),
    re_path(r'^reviews/add/$', views.review_create, name='review_create'),
    re_path(r'^promos/$', views.promos, name='promos'),
    re_path(r'^parts/$', views.part_list, name='part_list'),
    re_path(r'^parts/(?P<pk>\d+)/$', views.part_detail, name='part_detail'),
    re_path(r'^parts/create/$', views.part_create, name='part_create'),
    re_path(r'^parts/(?P<pk>\d+)/edit/$', views.part_update, name='part_update'),
    re_path(r'^parts/(?P<pk>\d+)/delete/$', views.part_delete, name='part_delete'),
    re_path(r'^buy/$', views.sale_create, name='sale_create'),
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^external-apis/$', views.external_apis, name='external_apis'),
    re_path(r'^stats/$', views.stats, name='stats'),
    re_path(r'^stats/chart.png$', views.sales_chart, name='sales_chart'),
    re_path(r'^api/parts/$', views.parts_api, name='parts_api'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='shop/registration/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]
