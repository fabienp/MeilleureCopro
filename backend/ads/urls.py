from django.urls import path
# from .views import stats_view
from ads import views

urlpatterns = [
    path('ads/stats', views.stats_view),
    path('ads', views.ads_add),
]
