
class DiceGameLogic:
    def __init__(self, session, figure_factories, user_coins):
        self.session = session
        self.figure_factories = figure_factories
        self.user_coins = user_coins

    def start_game(self, choice1, choice2, bet, guessed_number):
        """Main method that coordinates the game run."""
        fig1, fig2 = self._create_figures(choice1, choice2)
        roll1, roll2 = self._roll_dice(fig1, fig2)
        total = roll1 + roll2
        payout = self._calculate_payout(fig1, fig2, bet, total, guessed_number)
        new_balance = self.user_coins - bet + payout

        self._save_to_session({
            "figure1": choice1,
            "figure2": choice2,
            "bet": bet,
            "guessed_number": guessed_number,
            "roll1": roll1,
            "roll2": roll2,
            "total": total,
            "payout": payout,
            "new_balance": new_balance,
        })

        return {
            "rolls": (roll1, roll2),
            "total": total,
            "payout": payout,
            "new_balance": new_balance
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
    def _calculate_payout(fig1, fig2, bet, total, guessed_number):
        """Calculates payout based on game results."""
        min_faces = min(fig1.faces, fig2.faces)
        max_faces = max(fig1.faces, fig2.faces)
        multiplier = (min_faces + max_faces) / 10

        if total == guessed_number:
            return int(bet * (multiplier + 1))
        elif abs(total - guessed_number) == 1:
            return int(bet * multiplier)
        else:
            return 0

    def _save_to_session(self, data):
        """Saves game data to the session."""
        for key, value in data.items():
            self.session[key] = value
        self.session.modified = True
