from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from basket import views

urlpatterns = [
    path('trade/', views.TradeList.as_view(), name='trades'),
    path('trade/<int:pk>/', views.TradeDetail.as_view(), name='trade'),
    path('portfolio/',views.PortfolioList.as_view(), name='portfolios'),
    path('portfolio/<int:pk>/', views.PortfolioDetail.as_view(), name='portfolio'),
    path('returns/<int:pk>/', views.Returns.as_view(), name='returns'),
]