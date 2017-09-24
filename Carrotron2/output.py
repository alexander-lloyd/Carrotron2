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


class Motor(Output):
    pass


class StepperMotor(Motor):
    INTERNAL_STEPPER_ID = 0

    def __init__(self, board, pins):
        super(StepperMotor, self).__init__(board, pins)
        self.id = StepperMotor.INTERNAL_STEPPER_ID
        StepperMotor.INTERNAL_STEPPER_ID += 1


class StepperMotorULN2003(StepperMotor):
    def __init__(self, board, pins):
        super(StepperMotorULN2003, self).__init__(board, pins)
        if StepperMotor.INTERNAL_STEPPER_ID > 6:  # We've run out of ids!
            # TODO: Dont hard encode the maximum values. Depends on the stepper implementation
            raise Exception("Too Many Stepper Motors!")

        assert len(pins) == 4
        self.board.stepper_config(self.id,
                                  FirmataCommands.STEPPER_TYPES['FOUR_WIRE'],
                                  1024,
                                  pins
                                  )

    def step(self, direction, steps, speed):
        self.board.stepper_step(self.id, direction, steps, speed)


OUTPUTS = {
    "SG90": ServoSG90,
    "ULN2003": StepperMotorULN2003
}



if __name__ == '__main__':
    import time
    from Carrotron2.board.arduino import ArduinoBoard

    board = ArduinoBoard('COM3')
    time.sleep(1)
    s = ServoSG90(board, [7], reverse=True)
    s.set_degrees(90)
    time.sleep(1)
    # s.set_degrees()
    print("Complete")
    # time.sleep(1)
    # s.set_degrees(90)
    time.sleep(1)
