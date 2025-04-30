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
        try:
            result = {}
            for reel in range(num_reels):
                shuffled_symbols = random.sample(list(self.symbols), len(self.symbols))
                result[reel] = [self.backend_symbol_map.get(shuffled_symbols[i].name, i) for i in range(visible_rows)]
            return result
        except Exception as e:
            import logging
            logging.error(f"Error generating spin: {str(e)}")
            # Return a default result in case of error
            return {reel: [0] * visible_rows for reel in range(num_reels)}

    def _extract_horizontal_values(self, result):
        """Extract horizontal values from result dictionary."""
        horizontal_values = []
        for value in result.values():
            horizontal_values.append(value)
        return horizontal_values

    def _transpose_matrix(self, matrix):
        """Transpose a matrix (convert rows to columns and vice versa)."""
        rows, cols = len(matrix), len(matrix[0])
        transposed = [[""] * rows for _ in range(cols)]

        for x in range(rows):
            for y in range(cols):
                transposed[y][rows - x - 1] = matrix[x][y]

        return transposed

    def _reverse_rows(self, matrix):
        """Reverse each row in a matrix."""
        return [row[::-1] for row in matrix]

    @staticmethod
    def flip_horizontal(result):
        """Convert vertical reels to horizontal rows for win checking."""
        try:
            # Extract values from result dictionary
            horizontal_values = []
            for value in result.values():
                horizontal_values.append(value)

            # Get dimensions
            rows, cols = len(horizontal_values), len(horizontal_values[0])

            # Create transposed matrix
            transposed = [[""] * rows for _ in range(cols)]
            for x in range(rows):
                for y in range(cols):
                    transposed[y][rows - x - 1] = horizontal_values[x][y]

            # Reverse each row
            reversed_rows = [row[::-1] for row in transposed]
            return reversed_rows
        except Exception as e:
            import logging
            logging.error(f"Error in flip_horizontal: {str(e)}")
            return []

    @staticmethod
    def longest_seq(hit):
        """Find the longest sequence of consecutive indices."""
        try:
            if not hit:
                return []

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
        except Exception as e:
            import logging
            logging.error(f"Error finding longest sequence: {str(e)}")
            return []

    def _find_winning_combinations(self, horizontal):
        """Find winning combinations in horizontal rows."""
        hits = {}

        for row_index, row in enumerate(horizontal):
            for sym in set(row):  # Use set to process each symbol only once
                if row.count(sym) > self.MIN_SYMBOLS_FOR_WIN:
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]
                    longest = self.longest_seq(possible_win)

                    if len(longest) > self.MIN_SYMBOLS_FOR_WIN:
                        symbol_name = self.frontend_symbol_map.get(sym, f"symbol_{sym}")
                        hits[row_index + 1] = [symbol_name, longest]

        return hits

    def check_wins(self, result):
        """Check for winning combinations in the spin result."""
        try:
            horizontal = self.flip_horizontal(result)
            if not horizontal:
                return None

            hits = self._find_winning_combinations(horizontal)
            return hits if hits else None
        except Exception as e:
            import logging
            logging.error(f"Error checking wins: {str(e)}")
            return None

    def _get_symbol_multiplier(self, symbol_name):
        """Get the payout multiplier for a symbol with error handling."""
        try:
            from .models import Symbol
            symbol = Symbol.objects.get(name=symbol_name)
            return symbol.payout_multiplier
        except Symbol.DoesNotExist:
            import logging
            logging.warning(f"Symbol '{symbol_name}' not found, using default multiplier")
            return Decimal('1.0')
        except Exception as e:
            import logging
            logging.error(f"Error getting symbol multiplier: {str(e)}")
            return Decimal('1.0')

    def _calculate_win_payout(self, symbol_name, indices, bet_amount):
        """Calculate payout for a single winning combination."""
        combo_length = len(indices)
        multiplier = self._get_symbol_multiplier(symbol_name)
        return Decimal(bet_amount) * combo_length * multiplier

    def calculate_payout(self, win_data, bet_amount):
        """Calculate payout based on win data and bet amount."""
        try:
            if not win_data:
                return Decimal('0.00')

            total_payout = Decimal('0.00')

            for row_number, win_info in win_data.items():
                sym_name, indices = win_info
                win_payout = self._calculate_win_payout(sym_name, indices, bet_amount)
                total_payout += win_payout

            return total_payout
        except Exception as e:
            import logging
            logging.error(f"Error calculating payout: {str(e)}")
            return Decimal('0.00')


class SlotMachineService:
    def __init__(self):
        try:
            symbols = Symbol.objects.all()
            self.reel_service = ReelService(symbols)
            self.user = UserManager()
        except Exception as e:
            import logging
            logging.error(f"Error initializing SlotMachineService: {str(e)}")
            raise

    def _update_user_balance_for_bet(self, user, bet_amount):
        """Update user balance for a new bet with error handling."""
        try:
            # Check if user has profile
            if not hasattr(user, 'profile'):
                import logging
                logging.warning(f"User {user.id} does not have profile attribute")
                return False

            # Deduct from user's balance using the profile method
            user.profile.deduct_balance(Decimal(bet_amount))

            # Update total_wager if it exists
            if hasattr(user, 'total_wager'):
                user.total_wager += Decimal(bet_amount)
                user.save()

            return True
        except Exception as e:
            import logging
            logging.error(f"Error updating user balance for bet: {str(e)}")
            return False

    def _update_user_balance_for_win(self, user, payout):
        """Update user balance for a win with error handling."""
        try:
            # Check if user has profile
            if not hasattr(user, 'profile'):
                import logging
                logging.warning(f"User {user.id} does not have profile attribute")
                return False

            # Add to user's balance using the profile method
            user.profile.add_balance(payout)

            # Update total_won if it exists
            if hasattr(user, 'total_won'):
                user.total_won += payout
                user.save()

            return True
        except Exception as e:
            import logging
            logging.error(f"Error updating user balance for win: {str(e)}")
            return False

    def _create_spin_record(self, user, bet_amount, payout, result, win_data):
        """Create a spin record with error handling."""
        try:
            spin = Spin.objects.create(
                user=user,
                bet_amount=bet_amount,
                payout=payout,
                result=result,
                win_data=win_data
            )
            return spin
        except Exception as e:
            import logging
            logging.error(f"Error creating spin record: {str(e)}")
            return None

    def play_spin(self, user, bet_amount):
        """Process a single spin of the slot machine."""
        try:
            # Check if user has profile
            if not hasattr(user, 'profile'):
                import logging
                logging.warning(f"User {user.id} does not have profile attribute")
                return {
                    'success': False,
                    'message': 'User profile not available'
                }

            # Validate user balance
            if user.profile.balance < Decimal(bet_amount):
                return {
                    'success': False,
                    'message': 'Insufficient balance'
                }

            # Update user balance for bet
            if not self._update_user_balance_for_bet(user, bet_amount):
                return {
                    'success': False,
                    'message': 'Error processing bet'
                }

            # Generate spin result
            result = self.reel_service.generate_spin()

            # Check for wins
            win_data = self.reel_service.check_wins(result)
            payout = Decimal('0.00')

            # Process payout if there's a win
            if win_data:
                payout = self.reel_service.calculate_payout(win_data, bet_amount)
                if not self._update_user_balance_for_win(user, payout):
                    return {
                        'success': False,
                        'message': 'Error processing win'
                    }

            # Create spin record
            spin = self._create_spin_record(user, bet_amount, payout, result, win_data)
            if not spin:
                return {
                    'success': False,
                    'message': 'Error recording spin'
                }

            # Prepare response
            response = {
                'success': True,
                'spin_id': spin.id,
                'result': result,
                'win_data': win_data,
                'payout': payout
            }

            # Add current balance if profile is available
            if hasattr(user, 'profile'):
                response['current_balance'] = float(user.profile.balance)

            return response
        except Exception as e:
            import logging
            logging.error(f"Unexpected error in play_spin: {str(e)}")
            return {
                'success': False,
                'message': 'An unexpected error occurred'
            }
