from django.urls import path
from . import views
from .views import ClassroomListView, ProductListView

urlpatterns = [
    path('', views.classroom_view, name='classroom'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('classroom/', ClassroomListView.as_view(), name="classroom_api"),
    path('product/', ProductListView.as_view(), name="product_api")
]
