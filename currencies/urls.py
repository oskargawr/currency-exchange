from django.urls import path
from . import views


app_name = 'currencies'


urlpatterns = [
    path('', views.currency_list, name='currency_list'),
    path('favorites/', views.favorite_currencies, name='favorites'),
    path('favorites/add/<str:base>/', views.add_favorite, name='add_favorite'),
    path('favorites/remove/<str:base>/', views.remove_favorite, name='remove_favorite'),
    path('<str:base>/', views.currency_detail, name='detail'),

]
