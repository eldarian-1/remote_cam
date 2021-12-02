from django.test import TestCase


class CameraTestCases(TestCase):
    def setUp(self) -> None:
        self.one = 1

    def test_camera(self):
        self.assertEqual(self.one, 1)
