import pytest
from unittest.mock import patch, Mock
import telebot

from bot import start


class Telebot:
    @pytest.fixture(autouse=True)
    def setup_bot(self):
        self.bot = telebot.TeleBot('6654637783:AAEtmlyPK5biRGWj7iRdHeJkRs7N2Iu4_3g')
        self.message = Mock()

    def test_send_welcome(self):
        with patch('telebot.Telebot.replay_to') as mocked_replay_to:
            start(self.message)
            mocked_replay_to.assert_called_once_with(self.message, 'Нажать')

if __name__ == '__main__':
    pytest.main()

