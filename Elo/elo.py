from decimal import Decimal, getcontext

getcontext().prec = 6  # Set precision for Decimal calculations

def expected_score(raing_a, rating_b):
    exp_a = Decimal(1) / (Decimal(1) + Decimal(10) ** ((Decimal(rating_b) - Decimal(raing_a)) / Decimal(400)))
    return exp_a

def match_score(game_wins_a, game_wins_b, best_of):
    #BO1
    if best_of == 1:
        return Decimal("1.0") if game_wins_a > game_wins_b else Decimal("0.0")
    #BO3
    elif best_of == 3:
        mapping = {
            (2, 0): Decimal("1.0"),
            (2, 1): Decimal("0.75"),
            (1, 2): Decimal("0.25"),
            (0, 2): Decimal("0.0"),
        }
        return mapping[(game_wins_a, game_wins_b)]
    #BO5
    if best_of == 5:
        mapping = {
            (3, 0): Decimal("1.00"),
            (3, 1): Decimal("0.80"),
            (3, 2): Decimal("0.65"),
            (2, 3): Decimal("0.35"),
            (1, 3): Decimal("0.20"),
            (0, 3): Decimal("0.00"),
        }
        return mapping[(game_wins_a, game_wins_b)]
    raise ValueError("Invalid best_of value")

def calculate_elo(rating_a, rating_b, score_a, k):
    expected_a = expected_score(rating_a, rating_b)
    expected_b = expected_score(rating_b, rating_a)
    
    new_rating_a = rating_a + Decimal(k) * (score_a - expected_a)
    new_rating_b = rating_b + Decimal(k) * ((Decimal(1) - score_a) - expected_b)
    
    return new_rating_a, new_rating_b

def draw_elo(player1_elo, player2_elo, k=20):
    p1_expected = 1 / (1 + 10 ** ((player2_elo - player1_elo) / 400))
    p2_expected = 1 / (1 + 10 ** ((player1_elo - player2_elo) / 400))
    result= Decimal("0.5")

    player1_elo = player1_elo + k * (result - p1_expected)
    player2_elo = player2_elo + k * (result - p2_expected)

    return player1_elo, player2_elo