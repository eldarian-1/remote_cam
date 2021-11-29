from django.test import TestCase

from .views import VideoCamera

class CameraTestCases(TestCase):
    def setUp(self) -> None:
        self.camera = VideoCamera()
        self.one = 1

    def test_camera(self):
        self.assertEqual(self.one, 1)
