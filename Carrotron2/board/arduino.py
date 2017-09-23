from abc import abstractmethod
import logging
import math
from threading import Thread, Event
import time

from serial import Serial

from Carrotron2.board.base import Board, FirmataCommands

logger = logging.getLogger(__name__)

class Pin:
    def __init__(self, pin):
        self.pin = pin
        self.value = 0
        self.reporting = False



class BaseFirmata(Thread):
    def __init__(self, address, board):
        super(BaseFirmata, self).__init__()
        self.address = address
        self.board = board
        self.event = Event()

    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def read(self):
        pass


class FirmataUSBSerial(BaseFirmata):
    def __init__(self, address, board, baud_rate=57600):
        super(FirmataUSBSerial, self).__init__(address, board)
        self.serial = Serial(address, baudrate=baud_rate)
        self.currentBuffer = []
        self.version_received = False
        self.start()

    def write(self, data):
        self.serial.write(data)

    def read(self):
        # if self.buffer == []:
        #     return None
        # return self.buffer.pop()
        pass

    def run(self):
        while not self.serial.isOpen():
            time.sleep(0.1)
        logger.debug("Stream Opened on port: {port}".format(port=self.address))
        buffer = []
        while not self.event.is_set():
            buffer_size = self.serial.inWaiting()
            # print("Buffer size: ", buffer_size)
            if buffer_size:
                data_stream = self.serial.read(buffer_size) # TODO: Receive a chunk of data
                buffer.extend(data_stream)

            if len(buffer) > 0:
                # logger.debug("Read from Serial: {}".format(buffer))
                self.handle_message(buffer) # TODO If we read half way through message we'll cut it in half
                buffer.clear()

            time.sleep(0.01)
        self.serial.close()


    def handle_message(self, buffer):
        logger.debug("Handling: {}".format(buffer))
        for byte in buffer:
            if len(self.currentBuffer) == 0 and byte == 0:
                # Suspect this might cause issues if the currentBuffer is empty?
                continue  # Don't put  0 as the first byte on the buffer
            else:
                self.currentBuffer.append(byte)

                first = self.currentBuffer[0]
                last = self.currentBuffer[-1]

                # [START_SYSEX, ..., END_SYSEX]
                if first == FirmataCommands.START_SYSEX and last == FirmataCommands.END_SYSEX:
                    # handler = self.event_handler.sysex_response.get(self.currentBuffer[1])
                    sysex_command = self.currentBuffer[1]
                    handler_name = 'handle_sysex_' + FirmataCommands.COMMAND_TO_SYSEX.get(sysex_command, "not exist")
                    handler = getattr(self, handler_name, None)

                    if handler is not None and self.version_received:
                        # Make sure the sysex we received has a handler.
                        # We can only process this after we recieved REPORT_VERSION
                        handler(self.currentBuffer)
                    else:
                        logger.warning("Handler does not exist for sysex {}".format(hex(sysex_command)))

                    self.currentBuffer.clear()
                elif first == FirmataCommands.START_SYSEX and len(self.currentBuffer) > 0:
                    currByte = byte
                    if (currByte > 0x7F):
                        # New command after an uncomplete one
                        self.currentBuffer.clear()
                        self.currentBuffer.append(currByte)
                else:
                    if first != FirmataCommands.START_SYSEX:
                        if first < FirmataCommands.START_SYSEX:
                            response = first & FirmataCommands.START_SYSEX
                        else:
                            response = first

                        # Check first byte is valid
                        if (response != FirmataCommands.REPORT_VERSION) and (
                                    response != FirmataCommands.ANALOG_MESSAGE) and (
                                    response != FirmataCommands.DIGITAL_MESSAGE):
                            self.currentBuffer.clear()
                if len(self.currentBuffer) == 3 and first != FirmataCommands.START_SYSEX:
                    if first < FirmataCommands.START_SYSEX:
                        response = first & FirmataCommands.START_SYSEX
                    else:
                        response = first

                    handler_name = 'handle_midi_' + FirmataCommands.COMMAND_TO_HANDLER.get(response) or None
                    handler = getattr(self, handler_name, None)
                    if handler is not None:
                        if (self.version_received or first == FirmataCommands.REPORT_VERSION):
                            self.version_received = True
                            handler(self.currentBuffer)
                        self.currentBuffer.clear()
                    else:
                        logger.warning("Handler does not exist for command: {}. Got Handler: {}".format(str(hex(response)), handler_name))
                        self.currentBuffer.clear()

    def handle_midi_REPORT_VERSION(self, buffer):
        buffer.pop(0) # Remove the irelavent command
        logger.debug("Recieved Report Version: {buffer}".format(buffer=buffer))

    def handle_midi_ANALOG_MESSAGE(self, buffer):
        pin = buffer[0] & 0x0F
        value = buffer[1] | (buffer[2] << 7)

        logger.debug("Received Analog Message: pin: {pin} value: {value}".format(
            pin=pin, value=value
        ))

        self.board.analog_pins[pin].value = value



class FirmataSocket(BaseFirmata):
    def __init__(self, address, board):
        super(FirmataSocket, self).__init__(address, board)

    def write(self, data):
        pass

    def read(self):
        pass


class ArduinoBoard(Board):
    """Class for accessing an arduino.

    This is implemented using the firmata library. The arduino wil be loaded with
    the configurable firmata sketch. It implements:

    - report_version
    - analog_message
    - digital_message
    - sysex query firmware
    - sysex capability response


    TODO: Implement both Serial and Ethernet connection
    """

    SERIAL = 0
    ETHERNET = 1

    def __init__(self, address, connection_type=SERIAL):
        """

        Args:
            address (str): The COM port or IP Address of the
            connection_type (int): SERIAL or ETHERNET connection to raspberry PI

        Raises:
            IOError: If the connection_type is not one supported
        """
        self.address = address
        self.type = connection_type

        if self.type == ArduinoBoard.SERIAL:  # TODO: Change into dict
            self.stream = FirmataUSBSerial(address, self)
        elif self.type == ArduinoBoard.ETHERNET:
            self.stream = FirmataSocket(address, self)
        else:
            raise IOError("Unsupported connection type")

        self.analog_pins = [Pin(i) for i in range(16)] # TODO: Change depending on board
        self.digital_pins = [Pin(i) for i in range(54)]

        time.sleep(2) # Give Firmata some time to setup

    def analog_read(self, pin):
        """Read the value of an analogue pin

        Args:
            pin (int): The pin number to read the analogue value of

        Returns:
            int in range 0 - 1023 (10 bit accuracy)

        """
        pin = self.analog_pins[pin]

        if not pin.reporting:
            self.__write([
                FirmataCommands.REPORT_ANALOG | (pin.pin & 0x0F),
                FirmataCommands.HIGH
            ])
            pin.reporting = True
        return pin.value

    def analog_write(self, pin, value):
        """Set the value of an analogue pin

        Args:
            pin   (int): The pin number
            value (int): The value to set the pin. Between 0 and 1023 (10 bit accuracy)

        Returns:
            None
        """
        if pin > 15:
            data = [
                FirmataCommands.EXTENDED_ANALOG,
                pin,
                value & 0x7F,
                (value >> 0x7F)
            ]
            if value > 0x00004000:
                data.append((value >> 14) & 0x7F)
            if value > 0x00200000:
                data.append((value >> 21) & 0x7F)
            if value > 0x10000000:
                data.append((value >> 28) & 0x7F)
            self.__write_sysex(data)
        else:
            data = [
                FirmataCommands.ANALOG_MESSAGE | pin,
                value & 0x7F,
                (value >> 7) & 0x7F
            ]
            self.__write(data)

    servo_write = analog_write
    pwm_write = analog_write

    def digital_read(self, pin):
        """Read the value of an digital pin

        Args:
            pin (int): The pin number to read the analogue value of

        Returns:
            bool: True for pin value HIGH, False for pin value LOW

        """
        pass

    def digital_write(self, pin, value):
        """Set the value of an digital pin

        Args:
            pin   (int): The pin number
            value (bool): The value to set the pin. Between 0 for LOW and 1 for HIGH

        Returns:
            None
        """
        # port = pin >> 3
        # bit = 1 << (pin & 0x07)
        #
        # if value:
        #     port |= bit
        # else:
        #     port &= ~bit

        self.__write([
            FirmataCommands.DIGITAL_WRITE,
            pin,
            value
        ])

    def set_pin_mode(self, pin, mode):
        """
        :param pin: int. Pin Number
        :param mode: option from MODES dict
        :return:
        """
        self.__write([
            FirmataCommands.PIN_MODE,
            pin,
            mode
        ])

    def get_capability(self):
        # Warning this takes a long time to receive all the data
        self.__write_sysex([FirmataCommands.CAPABILITY_QUERY])

    def __write(self, data):
        logger.debug("Writing: {data}".format(data=data))
        self.stream.write(data)

    def __write_sysex(self, data):
        sysex = [FirmataCommands.START_SYSEX] + data + [FirmataCommands.END_SYSEX]
        self.__write(sysex)

    def servo_config(self, pin, min_pulse=544, max_pulse=4000):
        self.__write_sysex([
            FirmataCommands.SERVO_CONFIG,
            pin,
            min_pulse & 0x7F,
            (min_pulse >> 7) & 0x7F,
            max_pulse & 0x7F,
            (max_pulse >> 7) & 0x7F,
        ])

    # Stepper Functions
    def stepper_config(self, stepper_id, stepper_type, steps_per_rev, pins):
        assert stepper_type == len(pins)
        # 4 Wire Stepper type has a value of 4 etc. Check we get the right number of pins in list

        data = [
            FirmataCommands.STEPPER,
            FirmataCommands.STEPPER_CONFIG,
            stepper_id,
            stepper_type,
            steps_per_rev & 0x7E,
            (steps_per_rev >> 7) & 0x7F,
        ]
        data += pins

        self.__write_sysex(data)

    def stepper_step(self, stepper_id, direction, steps, speed, accel=0, decel=0):
        data = [
            FirmataCommands.STEPPER,
            FirmataCommands.STEPPER_STEP,
            stepper_id,
            direction,  # TODO: Direction does not seem to change
            steps & 0x7F,
            (steps >> 7) & 0x7F,
            (steps >> 14) & 0x7F,
            speed & 0x7F,
            (speed >> 7) & 0x7F
        ]
        if (accel > 0 or decel > 0):
            data.extend(
                [
                    accel & 0x7F, (accel >> 7) & 0x7F,
                    decel & 0x7F, (decel >> 7) & 0x7F
                ])
        self.__write_sysex(data)


def test_read():
    arduino = ArduinoBoard('COM3')
    for _ in range(100):
        # print(arduino.analog_read(0))
        arduino.analog_read(0)
        time.sleep(1)


def test_write():
    arduino = ArduinoBoard('COM3')
    arduino.set_pin_mode(13, FirmataCommands.MODES.get('OUTPUT'))
    while True:
        arduino.digital_write(13, True)
        time.sleep(0.5)
        arduino.digital_write(13, False)
        time.sleep(0.5)

def test_capability():
    arduino = ArduinoBoard('COM3')
    time.sleep(5)
    arduino.get_capability()

def test_servo():
    arduino = ArduinoBoard('COM3')
    time.sleep(5)
    arduino.servo_config(7, min_pulse=500, max_pulse=2400)
    time.sleep(1)
    arduino.servo_write(7, 0)
    time.sleep(1)
    arduino.servo_write(7, 90)
    time.sleep(1)
    arduino.servo_write(7, 180)
    time.sleep(1)
    arduino.servo_write(7, 90)

def test_stepper():
    arduino = ArduinoBoard('COM3')
    time.sleep(2)
    arduino.stepper_config(0, FirmataCommands.STEPPER_TYPES['FOUR_WIRE'], 1024, [26,27,28,29])

    for _ in range(20):
        arduino.stepper_step(0, FirmataCommands.STEPPER_CW, 512, 180)
        time.sleep(2)

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    test_read()