import unittest

from camera import Sensor, Recorder, Controller


# Objetivo: Software para camara de vigilancia
# Partes:
## sensor de movimiento --> simulado
##      algo ha empezado a moverse
##      llevamos X segundos en que nada se mueve
## grabador --> simulado
##      empezar a grabar
##      parar la grabacion
## controlador (software)
##      nuestro objetivo es programar esta pieza - NO es simulado


class CameraTests(unittest.TestCase):
    def test_asks_the_recorder_to_stop_recording_when_no_information_received_from_sensor(
        self,
    ):
        sensor = Sensor()  # mocks
        recorder = Recorder()  # mocks
        self.called = False

        def save_call():
            self.called = True

        recorder.is_detecting_motion = lambda: False
        recorder.stop_recording = save_call
        controller = Controller(sensor, recorder)

        controller.record_motion()

        self.assertTrue(self.called)

    def test_(self):
        self.assertEqual()

    def test_(self):
        self.assertEqual()

    def test_(self):
        self.assertEqual()

    def test_(self):
        self.assertEqual()

    def test_(self):
        self.assertEqual()

    def test_(self):
        self.assertEqual()

    def test_(self):
        self.assertEqual()
