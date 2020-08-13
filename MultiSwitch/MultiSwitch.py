# import pyvjoy
import threading
import pygame
import os
import time
import numpy as np

# TODO:
# class and instances ? of switched for DDU controls and iRacing controls
#   properites: name, name of RTDB value, type (Boolean or double/int), step, max, min
#   methods: increase, decrease
#   iRacing control specidic:
#       iRacing controlls need to be mapped via vJoy to increase and decrese funtions
# general Mutliswitch class
#   methods: initialise, add iRacing control, add DDU contol
#   properties: controls
#   runs infinitely, scanns for control inputs and processes this information
#   functions to calibrate iRacing controls
#   gui and function to set multi functions buttons
#   gui and function to populate iracing controls


class MultiSwitchItem:
    db = 0
    NButtonIncMap = 19
    NButtonDecMap = 20
    NButtonIncValue = 21
    NButtonDecValue = 22

    def __init__(self):
        pass

    @staticmethod
    def setDB(rtdb):
        MultiSwitchItem.db = rtdb


class MultiSwitchThread(MultiSwitchItem, threading.Thread):
    def __init__(self, rate):
        MultiSwitchItem.__init__(self)
        threading.Thread.__init__(self)
        self.rate = rate


class MultiSwitch(MultiSwitchThread):
    maps = {}

    def __init__(self, RTDB, rate):
        MultiSwitchThread.__init__(self, rate)
        MultiSwitchItem.setDB(RTDB)
        self.timeStr = ''
        # test0 = MultiSwitchItem()
        # test = MultiSwitchMap('blah')

        # myJoystick = None
        pygame.init()
        # SCREEN = pygame.display.set_mode((10, 10))

        # initialize joystick
        if os.environ['COMPUTERNAME'] == 'MARC-SURFACE':
            self.initJoystick('vJoy Device')
        else:
            self.initJoystick('FANATEC ClubSport Wheel Base')

    def run(self):
        temp = list(self.maps.keys())
        while 1:
            # observe input controller
            events = pygame.event.get()
            for event in events:
                # if event.type == pygame.KEYDOWN:
                #     print(pygame.key.name(event.key))
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == self.NButtonIncMap:
                        NCurrentMap = self.db.NCurrentMap + 1
                        if NCurrentMap > len(temp)-1:
                            NCurrentMap = NCurrentMap - len(temp)

                        self.db.NCurrentMap = NCurrentMap

                        print('Current map: {} . {}'.format(self.db.NCurrentMap, temp[self.db.NCurrentMap]))

                    elif event.button == self.NButtonDecMap:
                        NCurrentMap = self.db.NCurrentMap - 1
                        if NCurrentMap < 0:
                            NCurrentMap = len(temp) + NCurrentMap

                        self.db.NCurrentMap = NCurrentMap

                        print('Current map: {} . {}'.format(self.db.NCurrentMap, temp[self.db.NCurrentMap]))

                    elif event.button == self.NButtonIncValue:
                        self.maps[temp[self.db.NCurrentMap]].increase()
                    elif event.button == self.NButtonDecValue:
                        self.maps[temp[self.db.NCurrentMap]].decrease()

            # in case of relevant change inrease or decrese value and send
            # if iRacing Control forward command via vjoy

            # execute this loop while iRacing is running
            # print('running')
            # self.j.set_button(1,1)
            # time.sleep(self.rate)
            # self.j.set_button(1,0)
            # time.sleep(self.rate)

            time.sleep(self.rate)

    def initJoystick(self, name):
        pygame.joystick.init()
        print(self.timeStr + ': \t' + str(pygame.joystick.get_count()) + ' joysticks detected:')

        desiredJoystick = 9999

        for i in range(pygame.joystick.get_count()):
            print(self.timeStr + ':\tJoystick ', i, ': ', pygame.joystick.Joystick(i).get_name())
            if pygame.joystick.Joystick(i).get_name() == name:
                desiredJoystick = i

        if not desiredJoystick == 9999:
            print(self.timeStr + ':\tConnecting to', pygame.joystick.Joystick(desiredJoystick).get_name())
            myJoystick = pygame.joystick.Joystick(desiredJoystick)
            myJoystick.get_name()
            myJoystick.init()
            print(self.timeStr + ':\tSuccessfully connected to', pygame.joystick.Joystick(desiredJoystick).get_name(), '!')
        else:
            print(self.timeStr + ':\tFANATEC ClubSport Wheel Base not found!')

    def addMapping(self, name='name', minValue=0 , maxValue= 1, step=1):
        if name in self.db.dc:
            self.maps[name] = MultiSwitchMapiRControl(name, minValue , maxValue, step)
        else:
            self.maps[name] = MultiSwitchMapDDUControl(name, minValue , maxValue, step)

class MultiSwitchMapDDUControl(MultiSwitchItem):
    def __init__(self, name, minValue , maxValue, step):
        MultiSwitchItem.__init__(self)
        self.name = name
        self.type = type(self.db.__getattribute__(name))
        if self.type is not bool:
            self.minValue = minValue
            self.maxValue = maxValue
            self.step = step

    def increase(self):
        if self.type is not bool:
            newVal = np.min([self.db.__getattribute__(self.name) + self.step, self.maxValue])
            self.db.__setattr__(self.name, newVal)
        else:
            self.db.__setattr__(self.name, not self.db.__getattribute__(self.name))

        print('Increase ' + self.name)

    def decrease(self):
        if self.type is not bool:
            newVal = np.max([self.db.__getattribute__(self.name) - self.step, self.minValue])
            self.db.__setattr__(self.name, newVal)
        else:
            self.db.__setattr__(self.name, not self.db.__getattribute__(self.name))

        print('Decrease ' + self.name)

class MultiSwitchMapiRControl(MultiSwitchItem):
    def __init__(self, name, minValue , maxValue, step):
        MultiSwitchItem.__init__(self)
        self.name = name
        self.type = type(self.db.__getattribute__(name))
        if self.type is not bool:
            self.minValue = minValue
            self.maxValue = maxValue
            self.step = step

    def increase(self):
        print('Increase ' + self.name)

    def decrease(self):
        print('Decrease ' + self.name)
