from threading import Thread
import time
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
    def __init__(self):
        super(GameController, self).__init__()
        self.running = True
        self.__listeners = []
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
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
    def __init__(self):
        super().__init__()
        self.app = Flask(__name__,static_folder='/build')
        self.socketio = SocketIO(self.app)

        self.app.add_url_rule('/', view_func=self.index_page)
        self.socketio.on_event("subscribeToData", self.handle_subscription)

        self.start()

    def run(self):
        self.app.run(host='0.0.0.0', port=3001)

    def index_page(self):
        return self.app.send_static_file('index.html')

    def handle_subscription(self, message):
        data = {
            0: 77,
            45: 25,
            90: 75,
            135: 50,
            180: 30
        }
        self.socketio.emit("subscribeToData", data=data)


if __name__ == '__main__':
    # controller = GameController()
    # observer = ControllerObserver(controller)
    # # pygame.joystick.get_axis()
    # import time
    #
    # time.sleep(100)

    webapp = WebAppController()