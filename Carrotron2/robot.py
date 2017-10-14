class Pilot:
    def add_motor(self, motor):
        pass

class Robot:
    def __init__(self):
        self.board = None
        self.controller = None
        self.sensors = []
        self.pilot = Pilot()

    def add_controller(self, controller):
        self.controller = controller

    def add_board(self, board):
        self.board = board

    def add_sensor(self, sensor):
        self.sensors.append(sensor)
