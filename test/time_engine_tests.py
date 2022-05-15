import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock

from src.dao import ActivitySummary
from src.time_engine import TimeEngine, DEFAULT_ACTIVITY_START_DURATION


class TestTimeEngine(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_dao = Mock()
        self.engine = TimeEngine(self.mock_dao)

    def test_init_log(self):
        self.mock_dao.get_last_log.return_value = None
        test_time = datetime(2020, 1, 1, 12, 0, 0)
        self.engine.log_activity('some-act', test_time)

        self.mock_dao.create_act_today.assert_called_once_with('some-act', DEFAULT_ACTIVITY_START_DURATION)
        self.mock_dao.set_last_log.assert_called_once_with(test_time)

        self.assertEqual(len(self.mock_dao.method_calls), 3)

    def test_first_log_today(self):
        self.mock_dao.get_last_log.return_value = datetime(2020, 1, 1, 12, 0, 0)
        test_time = datetime(2020, 1, 2, 8, 0, 0)
        self.engine.log_activity('first-act-today', test_time)

        self.mock_dao.create_act_today.assert_called_once_with('first-act-today', DEFAULT_ACTIVITY_START_DURATION)
        self.mock_dao.set_last_log.assert_called_once_with(test_time)

        self.assertEqual(len(self.mock_dao.method_calls), 3)

    def test_invalid_last_log(self):
        self.mock_dao.get_last_log.return_value = datetime(2020, 1, 2, hour=12)

        # wrong day
        self.assertRaises(ValueError,
                          lambda: self.engine.log_activity('invalid-act1', datetime(2020, 1, 1, hour=12))
                          )
        # wrong time
        self.assertRaises(ValueError,
                          lambda: self.engine.log_activity('invalid-act2', datetime(2020, 1, 2, hour=11))
                          )
        self.assertEqual(len(self.mock_dao.method_calls), 2)

    def test_new_act_today(self):
        self.mock_dao.get_last_log.return_value = datetime(2020, 1, 1, hour=8)
        self.mock_dao.get_act_today.return_value = None

        test_time = datetime(2020, 1, 1, hour=9)
        self.engine.log_activity('new_act_today', test_time)

        self.mock_dao.get_act_today.assert_called_once_with('new_act_today')
        self.mock_dao.create_act_today.assert_called_once_with('new_act_today', timedelta(hours=1))
        self.mock_dao.set_last_log.assert_called_once_with(test_time)

        self.assertEqual(len(self.mock_dao.method_calls), 4)

    def test_extend_act_today(self):
        self.mock_dao.get_last_log.return_value = datetime(2020, 1, 1, hour=8)
        self.mock_dao.get_act_today.return_value = ActivitySummary('act_today', timedelta(hours=2))

        test_time = datetime(2020, 1, 1, hour=8, minute=15)
        self.engine.log_activity('act_today', test_time)

        self.mock_dao.get_act_today.assert_called_once_with('act_today')
        self.mock_dao.update_act_duration_today.assert_called_once_with('act_today', timedelta(hours=2, minutes=15))
        self.mock_dao.set_last_log.assert_called_once_with(test_time)

        self.assertEqual(len(self.mock_dao.method_calls), 4)
