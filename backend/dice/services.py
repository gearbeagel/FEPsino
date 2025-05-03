from decimal import Decimal
from django.db import transaction
from .dice import get_figure_factories
from .game_logic import DiceGameLogic
from .models import DiceGameModel


class DiceGameService:
    @staticmethod
    def execute_game_flow(user, data):
        with transaction.atomic():
            bet = Decimal(str(data['bet']))
            CoinService.check_user_coins(user, bet)
            CoinService.deduct_bet(user, bet)

            game_logic = DiceGameLogic(get_figure_factories(), user.profile.balance)
            result = game_logic.start_game(
                choice1=data['choice1'],
                choice2=data['choice2'],
                bet=bet,
                guessed_number=data['guessed_number']
            )
            DiceGameService.save_game_to_db(user, data, result)
            CoinService.update_balance(user, Decimal(str(result["payout"])))

        return result

    @staticmethod
    def save_game_to_db(user, data, result):
        """Persists the result of the game to the database."""
        DiceGameModel.objects.create(
            user=user,
            bet=Decimal(str(data['bet'])),
            guessed_number=data['guessed_number'],
            choice1=data['choice1'],
            choice2=data['choice2'],
            roll1=result['rolls'][0],
            roll2=result['rolls'][1],
            total=result['total'],
            payout=Decimal(str(result['payout'])),
        )

    @staticmethod
    def build_response(result, user):
        """Constructs the final response to be returned to the frontend."""
        return {
            "roll1": result["rolls"][0],
            "roll2": result["rolls"][1],
            "total": result["total"],
            "payout": result["payout"],
            "new_balance": user.profile.balance,
            "message": "You won!" if result["payout"] > 0 else "You lost."
        }


class CoinService:
    @staticmethod
    def check_user_coins(user, bet):
        """Check if the user has enough coins to place the bet."""
        if bet > user.profile.balance:
            raise ValueError('Not enough coins!')

    @staticmethod
    def deduct_bet(user, bet):
        """Deduct the bet amount from the user's balance."""
        user.profile.balance -= bet
        user.profile.save()

    @staticmethod
    def update_balance(user, payout):
        """Update the user's balance after the game."""
        user.profile.balance += payout
        user.profile.save()
