from django.urls import path
from . import views
from .views import ClassroomListView, ProductListView
# RequestManagementView
from .views import request_list, update_request_status

urlpatterns = [
    path('', views.classroom_view, name='classroom'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('classroom/', ClassroomListView.as_view(), name="classroom_api"),
    path('product/', ProductListView.as_view(), name="product_api"),
    # path('request_list/', RequestManagementView.as_view(), name="request_api"),
    # path('request_list/', request_list.as_view(), name='request_list'),
    # path('update_request_status/', update_request_status, name='update_request_status'),
    path('request_list/', request_list, name='request_list'),
    path('update_request_status/', update_request_status, name='update_request_status'),
]

