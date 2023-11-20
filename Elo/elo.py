def calculate_elo(winner_elo, loser_elo, k=20):
    winner_expected = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    loser_expected = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))
    
    winner_elo = winner_elo + k * (1 - winner_expected)
    loser_elo = loser_elo + k * (0 - loser_expected)
    
    return winner_elo, loser_elo