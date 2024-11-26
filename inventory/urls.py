from django.urls import path
from . import views
from .views import ClassroomListView

urlpatterns = [
    path('', views.inventory_view, name='inventory'),
    path('classroom/', ClassroomListView.as_view(), name="classroom_api")
]
