class Sensor:
    def is_detecting_motion(self) -> bool:
        pass


class Recorder:
    def start_recording(self):
        pass

    def stop_recording(self):
        pass


class Controller:

    sensor: Sensor  # dependency
    recorder: Recorder  # dependency

    def __init__(self, sensor, recorder):
        self.sensor = sensor
        self.recorder = recorder

    def record_motion(self):
        if self.sensor.is_detecting_motion():
            self.recorder.start_recording()
        else:
            self.recorder.stop_recording()
