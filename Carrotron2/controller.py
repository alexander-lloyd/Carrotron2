from threading import Thread
import pygame
from pygame import JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
pygame.joystick.init()

allowed_events = [JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION]

class ControllerObserver:
    def __init__(self, controller):
        controller.register_observer(self)

    def notify(self, observable, *args, **kwargs):
        print('Got', args, kwargs, 'From', observable)


class GameController(Thread):
    def __init__(self):
        self.running = True
        self.__listeners = []
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    def run(self):
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(allowed_events)

        while self.running:  # TODO: may need to change this
            for event in pygame.event.get():
                if event.type in allowed_events:
                    self.notify_observers(event.type, )
                self.notify_observers()
        pygame.joystick.quit()

    def stop(self):
        self.running = False

    def register_observer(self, controller_observer):
        self.__listeners.append(controller_observer)

    def notify_observers(self, *args, **kwargs):
        for listener in self.__listeners:
            listener.notify(self, *args, **kwargs)
