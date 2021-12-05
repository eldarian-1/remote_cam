from .logic import *
from datetime import timedelta
from django.test import TestCase


class CameraTestCases(TestCase):
    def setUp(self) -> None:
        pass

    def test_to_seconds(self):
        seconds = datetime(1970, 1, 1, 0, 0, 5, 0)
        self.assertEqual(to_seconds(seconds), 5)
        seconds = datetime(1970, 1, 1, 0, 5, 0, 0)
        self.assertEqual(to_seconds(seconds), 300)

    def test_diff_time(self):
        datetime_is_checking = datetime.now(timezone.utc) - timedelta(seconds=299)
        self.assertTrue(diff_time(datetime_is_checking))

    def test_filter_last_date(self):
        datetime_is_checking = datetime.now(timezone.utc) - timedelta(seconds=299)
        self.assertTrue(filter_last_date(datetime_is_checking, 300))
        self.assertFalse(filter_last_date(datetime_is_checking, 298))

    def test_does_user_exist(self):
        login, password = 'eldar', '12345678'
        create_user(login, password)
        self.assertTrue(does_user_exist(login, password))
        self.assertFalse(does_user_exist('login', 'password'))

    def test_attempts_left(self):
        self.assertEqual(attempts_left('login', 3, 300), (3, 0))

    def test_attempt_link(self):
        self.assertEqual(attempt_link('login'), '/?attempt_login=login')
        self.assertEqual(attempt_link('login with spaces'), '/?attempt_login=login+with+spaces')
        self.assertEqual(attempt_link('?id=6'), '/?attempt_login=%3Fid%3D6')
