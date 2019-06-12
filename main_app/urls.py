from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('games/', views.games_index, name='index'),
    path('games/<int:game_id>/', views.games_detail, name='detail'),
    path('games/create/', views.GameCreate.as_view(), name='games_create'),
    path('games/<int:pk>/update/', views.GameUpdate.as_view(), name='games_update'),
    path('games/<int:pk>/delete/', views.GameDelete.as_view(), name='games_delete'),
    path('games/<int:game_id>/add_played/', views.add_played, name='add_played'),
    path('games/<int:game_id>/add_photo/', views.add_photo, name='add_photo'),
    path('games/<int:game_id>/assoc_adj/<int:adj_id>/', views.assoc_adj, name='assoc_adj'),
    path('games/<int:game_id>/unassoc_adj/<int:adj_id>/', views.unassoc_adj, name='unassoc_adj'),
]