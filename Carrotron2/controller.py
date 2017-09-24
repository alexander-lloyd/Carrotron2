from threading import Thread
import time, random, threading
from flask import Flask
from flask_socketio import SocketIO

import pygame
from pygame import JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION

pygame.init()
pygame.joystick.init()

allowed_events = [JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION]


class ControllerObserver:
    def __init__(self, controller):
        controller.register_observer(self)

    def notify(self, observable, *args, **kwargs):
        print('Got', args, kwargs, 'From', observable)


class GameController(Thread):
    def __init__(self, robot):
        super(GameController, self).__init__()
        self.running = True
        self.__listeners = []
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.robot = robot
        self.start()

    def run(self):
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(allowed_events)

        pygame.joystick.Joystick(0).init()

        while self.running:  # TODO: may need to change this
            for event in pygame.event.get():
                if event.type in allowed_events:
                    self.notify_observers(event.type, )
            time.sleep(0.1)
        pygame.joystick.quit()

    def stop(self):
        self.running = False

    def register_observer(self, controller_observer):
        print("Registered Observer")
        self.__listeners.append(controller_observer)

    def notify_observers(self, *args, **kwargs):
        for listener in self.__listeners:
            listener.notify(self, *args, **kwargs)


class WebAppController(Thread):
    def __init__(self, robot):
        super(WebAppController, self).__init__()
        self.robot = robot
        self.app = Flask(__name__, static_folder='/build')
        self.socketio = SocketIO(self.app)

        self.app.add_url_rule('/', view_func=self.index_page)
        self.socketio.on_event("subscribeToData", self.handle_subscription)

        self.start()

    def run(self):
        self.app.run(host='0.0.0.0', port=3001)

    def index_page(self):
        return self.app.send_static_file('index.html')

    def handle_subscription(self, message):
        t = set_interval(self.handle_subscription_1, 0.1)
        # t.cancel()

    def handle_subscription_1(self):
        data = {
            90: self.robot.sensors[0].get_distance()
            # 0: random.randint(500, 700),
            # 45: random.randint(500, 700),
            # 90: random.randint(500, 700),
            # 135: random.randint(500, 700),
            # 180: random.randint(500, 700)
        }

        self.socketio.emit("subscribeToData", data=data)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

CONTROLLERS = {
    'WebApp': WebAppController,
    'USBController': GameController
}

if __name__ == '__main__':
    # controller = GameController()
    # observer = ControllerObserver(controller)
    # # pygame.joystick.get_axis()
    # import time
    #
    # time.sleep(100)

    webapp = WebAppController()
