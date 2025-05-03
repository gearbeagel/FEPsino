from dataclasses import dataclass
from decimal import Decimal

@dataclass
class GameContext:
    """Data class to hold the game context."""
    fig1: object
    fig2: object
    bet: int
    total: int
    guessed_number: int


class DiceGameLogic:
    PAYOUT_SCALE_FACTOR = 10

    def __init__(self, figure_factories, user_coins: Decimal):
        self.figure_factories = figure_factories
        self.user_coins = user_coins

    def start_game(self, choice1, choice2, bet, guessed_number):
        """Main method that coordinates the game run."""
        fig1, fig2 = self._create_figures(choice1, choice2)
        roll1, roll2 = self._roll_dice(fig1, fig2)
        total = roll1 + roll2
        context = GameContext(
            fig1=fig1,
            fig2=fig2,
            bet=bet,
            total=total,
            guessed_number=guessed_number
        )
        payout = self._calculate_payout(context)

        return {
            "rolls": (roll1, roll2),
            "total": total,
            "payout": payout,
        }

    def _create_figures(self, choice1, choice2):
        """Creates two dice based on the user's selection."""
        fig1 = self.figure_factories[choice1].create_figure()
        fig2 = self.figure_factories[choice2].create_figure()
        return fig1, fig2

    @staticmethod
    def _roll_dice(fig1, fig2):
        """Rolls two dice."""
        return fig1.roll(), fig2.roll()

    @classmethod
    def _calculate_payout(cls, ctx: GameContext):
        """Calculates payout based on game context."""
        min_faces = Decimal(ctx.fig1.faces)
        max_faces = Decimal(ctx.fig2.faces)
        multiplier = (min_faces + max_faces) / cls.PAYOUT_SCALE_FACTOR
        match ctx.total:
            case _ if ctx.total == ctx.guessed_number:
                return (ctx.bet * (multiplier + 1)).quantize(Decimal('0.01'))
            case _ if abs(ctx.total - ctx.guessed_number) == 1:
                return (ctx.bet * multiplier).quantize(Decimal('0.01'))
            case _:
                return Decimal('0.00')


