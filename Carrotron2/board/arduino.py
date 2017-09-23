from Carrotron2.board.base import Board


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
        """
        self.address = address
        self.type = connection_type

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
