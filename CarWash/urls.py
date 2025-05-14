from . import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path( 'admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('empleados/', views.empleados, name='empleados'),
    path('citas/', views.citas, name='citas'),
    path('bodega/', views.bodega, name='bodega'),
]
