
class DiceGame:
    def __init__(self, session, figure_factories, user_coins):
        self.session = session
        self.figure_factories = figure_factories
        self.user_coins = user_coins

    def start_game(self, choice1, choice2, bet, guessed_number):
        """ Runs the dice game logic."""
        fig1 = self.figure_factories[choice1].create_figure()
        fig2 = self.figure_factories[choice2].create_figure()

        self.session["figure1"] = choice1
        self.session["figure2"] = choice2
        self.session["bet"] = bet
        self.session["guessed_number"] = guessed_number
        self.session["roll1"] = fig1.roll()
        self.session["roll2"] = fig2.roll()

        total = self.session["roll1"] + self.session["roll2"]
        payout = self._calculate_payout(fig1, fig2, bet, total, guessed_number)

        new_balance = self.user_coins - bet + payout
        self.session["total"] = total
        self.session["payout"] = payout
        self.session["new_balance"] = new_balance

        self.session.modified = True

        return {
            "rolls": (self.session["roll1"], self.session["roll2"]),
            "total": total,
            "payout": payout,
            "new_balance": new_balance
        }

    @staticmethod
    def _calculate_payout(fig1, fig2, bet, total, guessed_number):
        """ Calculate the payout based on the game rules."""
        min_faces = min(fig1.faces, fig2.faces)
        max_faces = max(fig1.faces, fig2.faces)
        multiplier = (min_faces + max_faces) / 10

        if total == guessed_number:
            return int(bet * (multiplier + 1))
        elif abs(total - guessed_number) == 1:
            return int(bet * multiplier)
        else:
            return 0
