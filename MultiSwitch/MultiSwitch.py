import pyvjoy
import threading
import pygame
import os
import time

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
    def __init__(self, RTDB):
        self.db = RTDB


class MultiSwitchThread(MultiSwitchItem, threading.Thread):
    def __init__(self, RTDB, rate):
        MultiSwitchItem.__init__(self, RTDB)
        threading.Thread.__init__(self)
        self.rate = rate


class MultiSwitch(MultiSwitchThread):
    def __init__(self, RTDB, rate):
        MultiSwitchThread.__init__(self, RTDB, rate)
        self.timeStr = ''
        # self.rate = rate
        # self.db = RTDB
        self.j = pyvjoy.VJoyDevice(1)

        myJoystick = None
        pygame.init()
        SCREEN = pygame.display.set_mode((10, 10))

        # initialize joystick
        if os.environ['COMPUTERNAME'] == 'MARC-SURFACE':
            self.initJoystick('vJoy Device')
        else:
            self.initJoystick('FANATEC ClubSport Wheel Base')

    def run(self):
        while 1:
            # observe input controller
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))

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

