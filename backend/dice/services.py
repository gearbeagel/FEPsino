from .game_logic import DiceGameLogic
from .dice import get_figure_factories
from .models import DiceGameModel


class DiceGameService:

    @staticmethod
    def get_user_coins(session, data):
        """Retrieves the current number of user coins from the session."""
        return session.get('user_coins', data['user_coins'])

    @staticmethod
    def run_game_logic(session, user_coins, data):
        """Initializes the game logic and runs the main game sequence."""
        figure_factories = get_figure_factories()
        game = DiceGameLogic(session, figure_factories, user_coins)
        return game.start_game(
            choice1=data['choice1'],
            choice2=data['choice2'],
            bet=data['bet'],
            guessed_number=data['guessed_number']
        )

    @staticmethod
    def save_game_to_db(user, data, result):
        """Persists the result of the game to the database."""
        DiceGameModel.objects.create(
            user=user,
            bet=data['bet'],
            guessed_number=data['guessed_number'],
            choice1=data['choice1'],
            choice2=data['choice2'],
            roll1=result['rolls'][0],
            roll2=result['rolls'][1],
            total=result['total'],
            payout=result['payout'],
            new_balance=result['new_balance'],
        )

    @staticmethod
    def build_response(result):
        """Constructs the final response to be returned to the frontend."""
        return {
            "roll1": result["rolls"][0],
            "roll2": result["rolls"][1],
            "total": result["total"],
            "payout": result["payout"],
            "new_balance": result["new_balance"],
            "message": "You won!" if result["payout"] > 0 else "You lost."
        }
