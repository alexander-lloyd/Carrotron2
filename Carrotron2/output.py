from Carrotron2.board.base import FirmataCommands

class Output:
    def __init__(self, board, pins):
        self.board = board
        self.pins = pins

class Servo(Output):
    def __init__(self, board, pins, reverse=False):
        super(Servo, self).__init__(board, pins)
        self.reverse = reverse

    def set_degrees(self, degrees):
        pass


class ServoSG90(Servo):
    def __init__(self, board, pins, reverse=False):
        super(ServoSG90, self).__init__(board, pins, reverse=reverse)

        assert len(pins) == 1
        self.board.servo_config(self.pins[0], min_pulse=500, max_pulse=2400)

    def set_degrees(self, degrees):
        if self.reverse:
            degrees = 180 - degrees
        self.board.servo_write(self.pins[0], degrees)


if __name__ == '__main__':
    import time
    from Carrotron2.board.arduino import ArduinoBoard

    board = ArduinoBoard('COM3')
    time.sleep(1)
    s = ServoSG90(board, [7], reverse=True)
    s.set_degrees(180)
    time.sleep(1)
    s.set_degrees(0)
    print("Complete")
    # time.sleep(1)
    # s.set_degrees(90)
    time.sleep(1)