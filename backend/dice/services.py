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

            if user.profile.balance < bet:
                raise ValueError('Not enough coins!')
            user.profile.deduct_balance(bet)

            game_logic = DiceGameLogic(get_figure_factories(), user.profile.balance)
            result = game_logic.start_game(
                choice1=data['choice1'],
                choice2=data['choice2'],
                bet=bet,
                guessed_number=data['guessed_number']
            )

            DiceGameService.save_game_to_db(user, data, result)

            if result["payout"] > 0:
                user.profile.add_balance(Decimal(str(result["payout"])))

        return result

    @staticmethod
    def save_game_to_db(user, data, result):
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
        return {
            "roll1": result["rolls"][0],
            "roll2": result["rolls"][1],
            "total": result["total"],
            "payout": result["payout"],
            "new_balance": user.profile.balance,
            "message": "You won!" if result["payout"] > 0 else "You lost."
        }