from abc import abstractmethod, ABC

class FirmataCommands:
    ANALOG_MAPPING_QUERY = 0x69
    ANALOG_MAPPING_RESPONSE = 0x6A
    ANALOG_MESSAGE = 0xE0
    CAPABILITY_QUERY = 0x6B
    CAPABILITY_RESPONSE = 0x6C
    DIGITAL_MESSAGE = 0x90
    DIGITAL_WRITE = 0xF5
    END_SYSEX = 0xF7
    EXTENDED_ANALOG = 0x6F
    I2C_CONFIG = 0x78
    I2C_REPLY = 0x77
    I2C_REQUEST = 0x76
    I2C_READ_MASK = 0x18  # 0b00011000
    I2C_END_TX_MASK = 0x40  # 0b01000000
    ONEWIRE_CONFIG_REQUEST = 0x41
    ONEWIRE_DATA = 0x73
    ONEWIRE_DELAY_REQUEST_BIT = 0x10
    ONEWIRE_READ_REPLY = 0x43
    ONEWIRE_READ_REQUEST_BIT = 0x08
    ONEWIRE_RESET_REQUEST_BIT = 0x01
    ONEWIRE_SEARCH_ALARMS_REPLY = 0x45
    ONEWIRE_SEARCH_ALARMS_REQUEST = 0x44
    ONEWIRE_SEARCH_REPLY = 0x42
    ONEWIRE_SEARCH_REQUEST = 0x40
    ONEWIRE_WITHDATA_REQUEST_BITS = 0x3C
    ONEWIRE_WRITE_REQUEST_BIT = 0x20
    PIN_MODE = 0xF4
    PIN_STATE_QUERY = 0x6D
    PIN_STATE_RESPONSE = 0x6E
    PING_READ = 0x75
    PULSE_IN = 0x74
    PULSE_OUT = 0x73
    QUERY_FIRMWARE = 0x79
    REPORT_ANALOG = 0xC0
    REPORT_DIGITAL = 0xD0
    REPORT_VERSION = 0xF9
    SAMPLING_INTERVAL = 0x7A
    SERVO_CONFIG = 0x70
    SERIAL_MESSAGE = 0x60
    SERIAL_CONFIG = 0x10
    SERIAL_WRITE = 0x20
    SERIAL_READ = 0x30
    SERIAL_REPLY = 0x40
    SERIAL_CLOSE = 0x50
    SERIAL_FLUSH = 0x60
    SERIAL_LISTEN = 0x70
    START_SYSEX = 0xF0
    STEPPER = 0x72
    STEPPER_CONFIG = 0x00
    STEPPER_STEP = 0x01
    STRING_DATA = 0x71
    SYSTEM_RESET = 0xFF

    MAX_PIN_COUNT = 128

    MODES = dict(
        INPUT=0x00,
        OUTPUT=0x01,
        ANALOG=0x02,
        PWM=0x03,
        SERVO=0x04,
        SHIFT=0x05,
        I2C=0x06,
        ONEWIREx=0x07,
        STEPPER=0x08,
        SERIAL=0x0A,
        PULLUP=0x0B,
        IGNORE=0x7F,
        PING_READ=0x75,
        UNKNOWN=0x10,
    )

    COMMAND_TO_SYSEX = {
    }

    COMMAND_TO_HANDLER = {
        0xE0: "ANALOG_MESSAGE",
        0xF9: "REPORT_VERSION"

    }

class Board(ABC):
    """Interface of methods required by sensors"""
    @abstractmethod
    def analog_read(self, pin):
        """Read the value of an analogue pin

        Args:
            pin (int): The pin number to read the analogue value of

        Returns:
            int in range 0 - 1023 (10 bit accuracy)

        """
        pass

    @abstractmethod
    def analog_write(self, pin, value):
        """Set the value of an analogue pin

        Args:
            pin   (int): The pin number
            value (int): The value to set the pin. Between 0 and 1023 (10 bit accuracy)

        Returns:
            None
        """

    @abstractmethod
    def digital_read(self, pin):
        """Read the value of an digital pin

        Args:
            pin (int): The pin number to read the analogue value of

        Returns:
            bool: True for pin value HIGH, False for pin value LOW

        """
        pass

    @abstractmethod
    def digital_write(self, pin, value):
        """Set the value of an digital pin

        Args:
            pin   (int): The pin number
            value (bool): The value to set the pin. Between 0 for LOW and 1 for HIGH

        Returns:
            None
        """
