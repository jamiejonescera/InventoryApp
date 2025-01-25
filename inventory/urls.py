from django.urls import path
from . import views
from .views import ClassroomListView, ProductListView, RequestManagementView

urlpatterns = [
    path('', views.classroom_view, name='classroom'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('classroom/', ClassroomListView.as_view(), name="classroom_api"),
    path('product/', ProductListView.as_view(), name="product_api"),
    path('requests/', RequestManagementView.as_view(), name="request_api"),
    path('handle_request_action/', views.handle_request_action, name='handle_request_action'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
]
