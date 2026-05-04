from django.urls import path
from .views import ReportsListView, ReportsCreateView, OrdersView

urlpatterns = [
    path("reports/", ReportsListView.as_view()),
    path("reports/create/", ReportsCreateView.as_view()),
    path("orders/", OrdersView.as_view()),
]