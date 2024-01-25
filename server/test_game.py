# test_game.py

from game_logic import PokerGame

def main():
    poker_game = PokerGame()
    poker_game.start_game()

    while True:
        current_player = poker_game.players[poker_game.current_turn]

        # Display the last card played
        print(f"\nCurrent State: {current_player['name']}'s turn")
        print(f"Last card played: {poker_game.last_card_played}")

        # Display the player's hand
        poker_game.display_hand(current_player['name'])

        if current_player['name'] == 'User':
            poker_game.play_card(current_player['name'])
        else:
            # PC's automatic move logic
            pc_move = poker_game.generate_pc_move()
            print(f"PC played: {pc_move}")
            poker_game.play_card(current_player['name'], pc_move)

if __name__ == "__main__":
    main()
