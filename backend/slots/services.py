import random
from decimal import Decimal
from .models import Symbol
from .models import Spin

from user.models import UserManager


class ReelService:
    MIN_SYMBOLS_FOR_WIN = 2

    def __init__(self, symbols):
        self.symbols = symbols
        self.frontend_symbol_map = {
            0: 'star',  # Star icon
            1: 'heart',  # Heart icon
            2: 'cherry',  # Cherry icon
            3: 'gem',  # Gem icon
            4: 'citrus',  # Citrus icon
        }
        self.backend_symbol_map = {v: k for k, v in self.frontend_symbol_map.items()}

    def generate_spin(self, num_reels=5, visible_rows=3):
        """Generate a random spin result with 5 reels and 3 visible symbols per reel."""
        result = {}
        for reel in range(num_reels):
            shuffled_symbols = random.sample(list(self.symbols), len(self.symbols))
            result[reel] = [self.backend_symbol_map.get(shuffled_symbols[i].name, i) for i in range(visible_rows)]
        return result

    @staticmethod
    def flip_horizontal(result):
        """Convert vertical reels to horizontal rows for win checking."""
        horizontal_values = []
        for value in result.values():
            horizontal_values.append(value)

        rows, cols = len(horizontal_values), len(horizontal_values[0])
        hvals2 = [[""] * rows for _ in range(cols)]

        for x in range(rows):
            for y in range(cols):
                hvals2[y][rows - x - 1] = horizontal_values[x][y]

        hvals3 = [item[::-1] for item in hvals2]
        return hvals3

    @staticmethod
    def longest_seq(hit):
        """Find the longest sequence of consecutive indices."""
        sub_seq_length, longest = 1, 1
        start, end = 0, 0

        for i in range(len(hit) - 1):
            if hit[i] == hit[i + 1] - 1:
                sub_seq_length += 1
                if sub_seq_length > longest:
                    longest = sub_seq_length
                    start = i + 2 - sub_seq_length
                    end = i + 2
            else:
                sub_seq_length = 1

        return hit[start:end]

    def check_wins(self, result):
        """Check for winning combinations in the spin result."""
        hits = {}
        horizontal = self.flip_horizontal(result)

        for row in horizontal:
            for sym in row:
                if row.count(sym) > self.MIN_SYMBOLS_FOR_WIN:
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]

                    longest = self.longest_seq(possible_win)
                    if len(longest) > self.MIN_SYMBOLS_FOR_WIN:
                        symbol_name = self.frontend_symbol_map.get(sym, f"symbol_{sym}")
                        hits[horizontal.index(row) + 1] = [symbol_name, longest]

        return hits if hits else None

    def calculate_payout(self, win_data, bet_amount):
        """Calculate payout based on win data and bet amount."""
        if not win_data:
            return Decimal('0.00')

        from .models import Symbol
        total_payout = Decimal('0.00')

        for row_number, win_info in win_data.items():
            sym_name, indices = win_info
            try:
                symbol = Symbol.objects.get(name=sym_name)
                combo_length = len(indices)
                total_payout += Decimal(bet_amount) * combo_length * symbol.payout_multiplier
            except Symbol.DoesNotExist:
                combo_length = len(indices)
                default_multiplier = Decimal('1.0')
                total_payout += Decimal(bet_amount) * combo_length * default_multiplier

        return total_payout


class SlotMachineService:
    def __init__(self):
        symbols = Symbol.objects.all()
        self.reel_service = ReelService(symbols)
        self.user = UserManager()

    def play_spin(self, user, bet_amount):
        """Process a single spin of the slot machine."""
        if user.balance < Decimal(bet_amount):
            return {
                'success': False,
                'message': 'Insufficient balance'
            }

        user.balance -= Decimal(bet_amount)
        user.total_wager += Decimal(bet_amount)
        user.save()

        result = self.reel_service.generate_spin()

        win_data = self.reel_service.check_wins(result)
        payout = Decimal('0.00')

        if win_data:
            payout = self.reel_service.calculate_payout(win_data, bet_amount)
            user.balance += payout
            user.total_won += payout
            user.save()

        spin = Spin.objects.create(
            user=user,
            bet_amount=bet_amount,
            payout=payout,
            result=result,
            win_data=win_data
        )

        return {
            'success': True,
            'spin_id': spin.id,
            'result': result,
            'win_data': win_data,
            'payout': payout,
            'current_balance': float(user.balance)
        }
