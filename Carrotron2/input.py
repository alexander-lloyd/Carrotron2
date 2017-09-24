import math

from Carrotron2.board.base import FirmataCommands

class Sensor:
    def __init__(self, board, pins):
        self.board = board
        self.pins = pins


class InfraRedSensor(Sensor):
    def get_distance(self):
        pass

    def raw_data(self):
        pass

class InfraRedSensor2Y0A02(InfraRedSensor):
    def __init__(self, board, pins):
        super(InfraRedSensor2Y0A02, self).__init__(board, pins)
        assert len(pins) == 1
        self.board.set_pin_mode(pins[0], FirmataCommands.MODES['ANALOG'])

    def raw_data(self):
        return self.board.analog_read(self.pins[0])

    def get_distance(self):
        """Convert to mm"""
        value = self.raw_data()
        # Function seems to return inches so we convert to mm
        return math.exp(8.5841 - math.log(value))*25.4 # http://forum.arduino.cc/index.php?topic=311356.0
