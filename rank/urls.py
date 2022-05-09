from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('online/', views.onlineRanking),
    path('mobile/', views.mobileRanking),
    path('steam/', views.steamRanking),

    # 순위 정보 업데이트
    path('steam/reload', views.steamReload),
    path('mobile/reload', views.mobileReload),
    path('online/reload', views.onlineReload),
]