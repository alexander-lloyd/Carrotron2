import logging

try:
    import cmath as math
except ImportError:
    import math

from flask import Flask, current_app
from flask_socketio import SocketIO

from Carrotron2.board.arduino import ArduinoBoard
from Carrotron2.control.pilot import DifferentialPilot
from Carrotron2.output import MotorDriveL9110, ServoSG90

MOTOR_A_PINS = (4, 5)
MOTOR_B_PINS = (6, 7)
X_SERVO = (8,)
Y_SERVO = (9,)

board = ArduinoBoard('COM3')
leftmotor = MotorDriveL9110(board, MOTOR_A_PINS)
rightmotor = MotorDriveL9110(board, MOTOR_B_PINS)

config = {
    'SECRET_KEY': 'sglkaj;lgkjrfla',

    'robot': {
        'board': board,
        'leftmotor': leftmotor,
        'rightmotor': rightmotor,
        'driver': DifferentialPilot(board, leftmotor, rightmotor),
        'xservo': ServoSG90(board, X_SERVO),
        'yservo': ServoSG90(board, Y_SERVO),

        'X_JOYSTICK_SENSATIVITY': 1.0,  # Reduce these to reduce the rotation speed of robot.
        'Y_JOYSTICK_SENSATIVITY': 1.0,
    }
}

app = Flask(__name__)
app.config.from_object(config)
socket = SocketIO(app)


@socket.on('angles')
def new_angles(angles):
    """
    Should receive something like: (x, y)

    x & y should be between -90, 90
    """
    logging.debug("New angle. Received: {}".format(angles))

    x, y = angles

    with current_app as app:
        app.config['robot']['xservo'].set_degrees(x + 90)  # Servo wants between 0-180. we get -90 - 90
        app.config['robot']['yservo'].set_degrees(y + 90)


@socket.on('joystick')
def new_joystick(data):
    """
    Input should be:
        {
          'joystick0x': ... # range 0-1
          'joystick0y': ... # range 0-1
        }
    """

    joystick_x = data['joystick0x']
    joystick_y = data['joystick0y']

    left_speed = 0
    right_speed = 0

    if joystick_x > 0:
        if joystick_y > 0:
            right_speed = joystick_y
        else:
            right_speed = -joystick_y
        left_speed = (joystick_x ** 2 + joystick_y ** 2) ** 0.5
    else:
        if joystick_y > 0:
            left_speed = joystick_y
        else:
            left_speed = -joystick_y
        right_speed = (joystick_x ** 2 + joystick_y ** 2) ** 0.5

    with current_app as app:
        app.config['robot']['leftmotor'].set_speed(left_speed)
        app.config['robot']['rightmotor'].set_speed(right_speed)


if __name__ == '__main__':
    app.run()
