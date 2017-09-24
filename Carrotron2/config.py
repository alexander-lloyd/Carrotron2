from yaml import load

try:
    from yaml import CLoader as Loader  # If its there, take advantage of the faster LibYAML loader
except ImportError:
    from yaml import Loader  # No LibYAML, use pure

from Carrotron2.robot import Robot
from Carrotron2.board import BOARDS
from Carrotron2.controller import CONTROLLERS
from Carrotron2.input import INPUTS
from Carrotron2.output import OUTPUTS


def load_yaml(str_or_buffer):
    """
    Load a yaml file or string and convert to dict
    """
    return load(str_or_buffer, Loader=Loader)


def load_yaml_from_file(filename):
    """
    Loads an environment file from file system
    """
    return load_yaml(open(filename))

def load_robot_config(filename):
    yaml = load_yaml_from_file(filename)
    print(yaml)
    r = Robot()
    robot = yaml['Robot']
    board = BOARDS.get(robot['board'])('COM3') # TODO
    r.add_board(board)

    controller = robot['controller']
    controller_object = CONTROLLERS[controller]
    c = controller_object(r)
    r.add_controller(c)


    for element, attr in robot.items():
        if element == 'Wheel':
            motor = attr['StepperMotor']
            motor_obj = OUTPUTS[motor['driver']](board, motor['pins'])
            r.pilot.add_motor(motor_obj)

        elif element == 'sensors':
            for sensor_type, sensor_data in attr.items():
                sensor = INPUTS.get(sensor_data['type'])
                sensor_obj = sensor(board, sensor_data['pins'])
                r.add_sensor(sensor_obj)

if __name__ == '__main__':
    load_robot_config('carrotron2.yaml')
