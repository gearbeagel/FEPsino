from dataclasses import dataclass


@dataclass
class GameContext:
    """Data class to hold the game context."""
    fig1: object
    fig2: object
    bet: int
    total: int
    guessed_number: int


class DiceGameLogic:
    def __init__(self, figure_factories, user_coins):
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
        user_coins = self.user_coins - bet + payout

        return {
            "rolls": (roll1, roll2),
            "total": total,
            "payout": payout,
            "user_coins": user_coins
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

    @staticmethod
    def _calculate_payout(ctx: GameContext):
        """Calculates payout based on game context."""
        min_faces = min(ctx.fig1.faces, ctx.fig2.faces)
        max_faces = max(ctx.fig1.faces, ctx.fig2.faces)
        multiplier = (min_faces + max_faces) / 10

        match ctx.total:
            case _ if ctx.total == ctx.guessed_number:
                return int(ctx.bet * (multiplier + 1))
            case _ if abs(ctx.total - ctx.guessed_number) == 1:
                return int(ctx.bet * multiplier)
            case _:
                return 0

