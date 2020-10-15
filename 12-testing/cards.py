def who_wins(cards_player1, cards_player2):
    ranking = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
        "1": 14,
    }
    if (
        len(cards_player1) != len(cards_player2)
        or len(cards_player1) == 0
        or len(cards_player2) == 0
    ):
        raise ValueError("The number of cards must be equal for both players")
    score_player1 = 0
    score_player2 = 0
    number_of_rounds = len(cards_player1)
    for each_round in range(number_of_rounds):
        if ranking[cards_player1[each_round]] > ranking[cards_player2[each_round]]:
            score_player1 += 1
        elif ranking[cards_player1[each_round]] < ranking[cards_player2[each_round]]:
            score_player2 += 1
    return format_final_score(score_player1, score_player2)


def format_final_score(score_player1, score_player2):
    if score_player1 > score_player2:
        return f"Player1 wins {score_player1} to {score_player2}"
    elif score_player1 < score_player2:
        return f"Player2 wins {score_player2} to {score_player1}"
    else:
        return "Tie"
