from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.board_list),
    path('write/', views.board_write),
    path('detail/<int:pk>/', views.board_detail),
    path('update/<int:pk>/', views.board_update),
    path('delete/<int:pk>/', views.board_delete),
    path('update/fail/', views.board_update_fail),
    path('delete/fail/', views.board_delete_fail),
    path('detail/<int:pk>/comment_delete/<int:ck>/', views.comment_delete),
]