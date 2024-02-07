from django.urls import path
import Elo.views

urlpatterns = [
    path('players/', Elo.views.PlayerList.as_view(), name='players'),
    path('players/<int:pk>/', Elo.views.PlayerDetail.as_view(), name='player-detail'),
    path('result/', Elo.views.ResultView.as_view(), name='result'),
    path('draw/', Elo.views.DrawView.as_view(), name='draw'),
    path('login/', Elo.views.LoginView.as_view(), name='login'),
    path('new/', Elo.views.GetNewIDView.as_view(), name='new'),
    path('filterPlayers/', Elo.views.PlayerFilterView.as_view(), name='filter-players'), 
]

