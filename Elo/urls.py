from django.urls import path
from .views import PlayerList, PlayerDetail, ResultView, GetNewIDView, PlayerFilterView

urlpatterns = [
    path('players/', PlayerList.as_view(), name='players'),
    path('players/<int:pk>/', PlayerDetail.as_view(), name='player-detail'),
    path('result/', ResultView.as_view(), name='result'),
    path('new/', GetNewIDView.as_view(), name='new'),
    path('filterPlayers/', PlayerFilterView.as_view(), name='filter-players'), 
]

