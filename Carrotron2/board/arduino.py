from abc import ABC, abstractmethod
import logging
from threading import Thread, Event
import time

from serial import Serial

from Carrotron2.board.base import Board, FirmataCommands

logger = logging.getLogger(__name__)


class BaseFirmata(Thread):
    def __init__(self, address):
        super(BaseFirmata, self).__init__()
        self.address = address
        self.event = Event()

    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def read(self):
        pass


class FirmataUSBSerial(BaseFirmata):
    def __init__(self, address, baud_rate=57600):
        super(FirmataUSBSerial, self).__init__(address)
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
            if self.serial.inWaiting():
                data = self.serial.read()
                buffer.append(data)

            if len(buffer) > 0:
                # logger.debug("Read from Serial: {}".format(buffer))
                self.handle_message(buffer) # TODO If we read half way through message we'll cut it in half
                buffer.clear()

            time.sleep(0.05)
        self.serial.close()


    def handle_message(self, buffer):
        logger.debug("Handling: {}".format(buffer))
        int_buffer = map(ord, buffer)
        for byte in int_buffer:
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
                        logger.warning("Handler does not exist for sysex {}".format(sysex_command))

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



class FirmataSocket(BaseFirmata):
    def __init__(self, address):
        super(FirmataSocket, self).__init__(address)

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
            self.stream = FirmataUSBSerial(address)
        elif self.type == ArduinoBoard.ETHERNET:
            self.stream = FirmataSocket(address)
        else:
            raise IOError("Unsupported connection type")

    def analog_read(self, pin):
        """Read the value of an analogue pin

        Args:
            pin (int): The pin number to read the analogue value of

        Returns:
            int in range 0 - 1023 (10 bit accuracy)

        """
        pass

    def analog_write(self, pin, value):
        """Set the value of an analogue pin

        Args:
            pin   (int): The pin number
            value (int): The value to set the pin. Between 0 and 1023 (10 bit accuracy)

        Returns:
            None
        """
        pass

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

    def __write(self, data):
        logger.debug("Writing: {data}".format(data=data))
        self.stream.write(data)

    def __write_sysex(self, data):
        sysex = [FirmataCommands.START_SYSEX] + data + [FirmataCommands.END_SYSEX]
        self.__write(sysex)

def test_read():
    arduino = ArduinoBoard('COM3')
    time.sleep(5)
    arduino.set_pin_mode(13, FirmataCommands.MODES.get('OUTPUT'))
    while True:
        arduino.digital_write(13, True)
        time.sleep(0.5)
        arduino.digital_write(13, False)
        time.sleep(0.5)


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    test_read()