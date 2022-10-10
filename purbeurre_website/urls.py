from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_account/', views.create_account, name='create_account'),
    path('login_user/', views.login_user, name='login_user'),
    path('user_account/', views.user_account, name='user_account'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('product_data/', views.product_data, name='product_data'),
    path('display_favourite/', views.display_favourite, name='display_favourite'),
    path('add_favourite/', views.add_favourite, name='add_favourite'),
    path('propose_substitute/', views.propose_substitute, name='propose_substitute'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('admin/', admin.site.urls)
]
