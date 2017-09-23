from abc import abstractmethod, ABC


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
