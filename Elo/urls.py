from django.urls import path
import elo.views

urlpatterns = [
    path('players/', elo.views.PlayerList.as_view(), name='players'),
    path('players/<int:pk>/', elo.views.PlayerDetail.as_view(), name='player-detail'),
    path('result/', elo.views.ResultView.as_view(), name='result'),
    path('draw/', elo.views.DrawView.as_view(), name='draw'),
    path('new/', elo.views.GetNewIDView.as_view(), name='new'),
    path('filterPlayers/', elo.views.PlayerFilterView.as_view(), name='filter-players'), 
    path('login/', elo.views.LoginView.as_view(), name='login'),
]

