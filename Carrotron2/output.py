from abc import abstractmethod

from Carrotron2.board.base import FirmataCommands


class Output:
    def __init__(self, board, pins):
        self.board = board
        self.pins = pins

class LED(Output):
    pass

class RBGLED(LED):
    def __init__(self, board, pins):
        super(RBGLED, self).__init__(board, pins)
        self.red_pin = pins[0]
        self.green_pin = pins[1]
        self.blue_pin = pins[2]

        self.board.set_pin_mode(self.red_pin, FirmataCommands.MODES['PWM'])
        self.board.set_pin_mode(self.green_pin, FirmataCommands.MODES['PWM'])
        self.board.set_pin_mode(self.blue_pin, FirmataCommands.MODES['PWM'])

    def set_color(self, rgb):
        """
        Args:
            rgb: Tuple of ints. between 0 and 255

        Returns:

        """
        r, g, b = rgb
        print(r, g, b)

        self.board.analog_write(self.red_pin, r)
        self.board.analog_write(self.green_pin, g)
        self.board.analog_write(self.blue_pin, b)



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
    @abstractmethod
    def forward(self):
        pass

    @abstractmethod
    def backwards(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class MotorDriveL9110(Motor):
    BACKWARDS = 0
    FORWARDS = 1

    def __init__(self, board, pins):
        super(MotorDriveL9110, self).__init__(board, pins)
        assert len(self.pins) == 2
        self.motor_outputs = dict(
            inputA = self.pins[0],
            inputB = self.pins[1])

        for pin in self.motor_outputs.values():
            self.board.set_pin_mode(pin, FirmataCommands.MODES['PWM'])

        self._speed = 100
        self._direction = MotorDriveL9110.FORWARDS # Default to forwards

    def forward(self):
        self.board.analog_write(self.motor_outputs['inputB'], 0)

    def backwards(self):
        self.board.analog_write(self.motor_outputs['inputA'], 0)
        # self.set_speed(self._speed)


    def stop(self):
        self.board.analog_write(self.motor_outputs['inputA'], 0)
        self.board.analog_write(self.motor_outputs['inputB'], 0)


    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = min(abs(int(speed)), 255) # TODO Dont hard encode 255


        if speed > 0:
            self._direction = MotorDriveL9110.FORWARDS
            self.board.analog_write(self.motor_outputs['inputA'], self._speed)
        else:
            self._direction = MotorDriveL9110.BACKWARDS
            self.board.analog_write(self.motor_outputs['inputB'], self._speed)



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
    import logging
    # logging.getLogger('Carrotron2.board.arduino').setLevel(logging.DEBUG)
    # logging.getLogger('Carrotron2.board.arduino').addHandler(logging.StreamHandler())
    from Carrotron2.board.arduino import ArduinoBoard

    board = ArduinoBoard('COM3')
    time.sleep(1)
    # s = ServoSG90(board, [8], reverse=True)
    # s.set_degrees(180)
    # time.sleep(1)
    # s.set_degrees(0)
    # print("Complete")
    # time.sleep(1)
    # s.set_degrees(90)
    # time.sleep(1)
    # # s.set_degrees()
    # print("Complete")
    # # time.sleep(1)
    # # s.set_degrees(90)
    # time.sleep(1)



    # left_motor = MotorDriveL9110(board, [4,5])
    # print("Created motor")
    # print("Forward")
    # left_motor.forward()
    # time.sleep(3)
    # print("Stop")
    # left_motor.stop()
    # left_motor.speed = 200
    # left_motor.backwards()
    # time.sleep(2)
    # left_motor.stop()

    # led = RBGLED(board, [10,11,12])
    # for _ in range(10):
    #     led.set_color((255, 0, 0)) # red
    #     time.sleep(1)
    #     led.set_color((0,0,0)) # no colour
    #     time.sleep(1)
    #     led.set_color((0, 255, 0)) # green
    #     time.sleep(1)
    #     led.set_color((0,0,0)) # no colour
    #     time.sleep(1)


    #Motor control

    motor = MotorDriveL9110(board, (4,5))
    input()
    motor.speed = 255
    motor.forward()
    speed = 255
    while motor.speed > 1:
        time.sleep(2)
        print(motor.speed)
        motor.speed /= 2
    exit()