import os
from unittest.mock import patch
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import Client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


class DiceGameTestCase(TestCase):
    @patch('rest_framework.test.APIClient.post')
    def test_dice_game(self, mock_post):
        mock_response = {
            "rolls": [1, 2, 3],
            "total": 6,
            "payout": 20,
            "new_balance": 110
        }
        mock_post.return_value.status_code = status.HTTP_200_OK
        mock_post.return_value.data = mock_response

        url = "/api/dice/start/"
        data = {
            "choice1": "1",
            "choice2": "2",
            "bet": 10,
            "guessed_number": 7,
            "user_coins": 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("rolls", response.data)
        self.assertIn("total", response.data)
        self.assertIn("payout", response.data)
        self.assertIn("new_balance", response.data)


class DiceGameTests(APITestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('dice_game')
        self.data = {
            "user_coins": 100,
            "choice1": "1",
            "choice2": "2",
            "bet": 20,
            "guessed_number": 10
        }

    def test_start_game_successful(self):
        with patch('dice.views.DiceGame') as mock_facade:
            mock_facade.return_value.start_game.return_value = {
                "rolls": [4, 6],
                "total": 10,
                "payout": 48,
                "new_balance": 128
            }
            response = self.client.post(self.url, self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('rolls', response.data)
            self.assertIn('total', response.data)
            self.assertIn('payout', response.data)
            self.assertIn('new_balance', response.data)

    def test_start_game_invalid_data(self):
        invalid_data = self.data.copy()
        invalid_data["bet"] = -10
        with patch('dice.views.DiceGame') as mock_facade:
            mock_facade.return_value.start_game.return_value = {
                "error": "Invalid bet amount"
            }
            response = self.client.post(self.url, invalid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)