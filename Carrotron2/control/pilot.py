

class DifferentialPilot:
    def __init__(self, board, leftmotor, rightmotor):
        self.board = board
        self.leftmotor = leftmotor
        self.rightmotor = rightmotor

        self.__current_angle = 0

    # def rotate(self, angle):
    #     # If we are at an angle of 50 degrees and this function is called with value 70 we need to move right 20 degrees.
    #
    #     angle_to_move = abs(self.__current_angle - angle) # Difference in angle
    #
    #     move_left = angle < self.__current_angle # Do we move left?
    #
    #     if move_left:
    #         # Left motor backwards, right forwards
    #         pass
    #     else: # move right
    #         # Left forwards, right backwards
    #         pass
    #
    #
    #     self.__current_angle = self.__current_angle - angle

    def set_rotation_speed(self, rotation_speed):
        self.leftmotor.speed = rotation_speed
        self.rightmotor.speed = - rotation_speed
