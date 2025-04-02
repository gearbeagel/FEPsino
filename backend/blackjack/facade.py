from .game_logic import BlackjackGame, Card
from user.models import User


class BlackjackGameFacade:


    def __init__(self, user):
        self.user = user
        self.profile = type('obj', (object,), {'balance': 1000, 'save': lambda: None})

    def get_game_state(self, session):

        game_state = session.get('game')
        bet = session.get('bet', 0)

        if not game_state:

            game = BlackjackGame()
            game.create_deck()
            game.dealer_hand = [game.deal_card()]
            session['game'] = game.get_game_state()
            game_state = session['game']

        return {
            'game_state': game_state,
            'balance': self.profile.balance,
            'bet': bet
        }

    def start_new_game(self, session):

        session['game'] = None
        session['bet'] = 0
        return self.get_game_state(session)

    def deal_cards(self, session):
        if 'game' not in session:

            game = BlackjackGame()
            game.create_deck()
            game.start_game()


            session['game'] = {
                'player_hand': [card.to_dict() for card in game.player_hand],
                'dealer_hand': [card.to_dict() for card in game.dealer_hand],
                'game_over': game.game_over
            }
        else:

            game_state = session['game']
            game = BlackjackGame()


            if 'deck' not in game_state:
                game.create_deck()
            else:
                game.deck = [Card(**card) for card in game_state['deck']]

            game.player_hand = [Card(**card) for card in game_state['player_hand']]
            game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]
            game.game_over = game_state['game_over']


        if not game.game_over:
            game.player_hand.append(game.deal_card())
            game.player_hand.append(game.deal_card())


            game.dealer_hand.append(game.deal_card())


        session['game'] = {
            'player_hand': [card.to_dict() for card in game.player_hand],
            'dealer_hand': [card.to_dict() for card in game.dealer_hand],
            'game_over': game.game_over
        }

        return {
            'game_state': session['game'],
            'balance': self.profile.balance,
            'bet': session.get('bet', 0)
        }

    def player_hit(self, session):

        game = BlackjackGame()
        game_state = session['game']


        game.player_hand = [Card(**card) for card in game_state['player_hand']]
        game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]
        game.game_over = game_state['game_over']

        result = game.player_hit()
        session['game'] = game.get_game_state()


        if result == "Bust! You lose.":
            bet = session.get('bet', 0)
            self.profile.balance -= bet
            self.profile.save()
            session['bet'] = 0

        return {
            'game_state': session['game'],
            'balance': self.profile.balance,
            'bet': session.get('bet', 0),
            'message': result
        }

    def player_stay(self, session):

        game = BlackjackGame()
        game_state = session['game']


        game.player_hand = [Card(**card) for card in game_state['player_hand']]
        game.dealer_hand = [Card(**card) for card in game_state['dealer_hand']]


        result = game.dealer_play()
        session['game'] = game.get_game_state()


        bet = session.get('bet', 0)
        if "You win" in result:
            self.profile.balance += bet * 2
        elif "Dealer wins" in result:
            self.profile.balance -= bet
        elif "tie" in result.lower():
            self.profile.balance += bet

        self.profile.save()
        session['bet'] = 0

        return {
            'game_state': session['game'],
            'balance': self.profile.balance,
            'bet': session['bet'],
            'message': result
        }

    def place_bet(self, session, amount):
        amount = int(amount)
        current_bet = session.get('bet', 0)

        if amount == 0:

            self.profile.balance += current_bet
            session['bet'] = 0
        elif self.profile.balance >= amount:

            session['bet'] = current_bet + amount
            self.profile.balance -= amount

        self.profile.save()

        return {
            'balance': self.profile.balance,
            'bet': session.get('bet', 0),
            'game_state': session.get('game')
        }