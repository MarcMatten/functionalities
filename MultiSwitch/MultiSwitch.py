import pyvjoy
import threading
import pygame
import os

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

class MultiSwitch(threading.Thread):
    def __init__(self, RTDB, rate):
        threading.Thread.__init__(self)
        self.rate = rate
        self.db = RTDB
        self.j = pyvjoy.VJoyDevice(1)

        myJoystick = None
        pygame.init()

        # initialize joystick
        if os.environ['COMPUTERNAME'] == 'MARC-SURFACE':
            self.initJoystick('vJoy Device')
        else:
            self.initJoystick('FANATEC ClubSport Wheel Base')

    def run(self):
        while 1:
            # observe input controller

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.db.StopDDU = True

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.JOYBUTTONDOWN and event.button == 25:
                    if self.db.NDDUPage == 1:
                        self.db.NDDUPage = 2
                    else:
                        self.db.NDDUPage = 1

            # in case of relevant change inrease or decrese value and send
            # if iRacing Control forward command via vjoy



            # execute this loop while iRacing is running
            # print('running')
            # self.j.set_button(1,1)
            # time.sleep(self.rate)
            # self.j.set_button(1,0)
            # time.sleep(self.rate)

    def initJoystick(self, name):
        pygame.joystick.init()
        print(self.db.timeStr + ': \t' + str(pygame.joystick.get_count()) + ' joysticks detected:')

        desiredJoystick = 9999

        for i in range(pygame.joystick.get_count()):
            print(self.db.timeStr + ':\tJoystick ', i, ': ', pygame.joystick.Joystick(i).get_name())
            if pygame.joystick.Joystick(i).get_name() == name:
                desiredJoystick = i

        if not desiredJoystick == 9999:
            print(self.db.timeStr + ':\tConnecting to', pygame.joystick.Joystick(desiredJoystick).get_name())
            myJoystick = pygame.joystick.Joystick(desiredJoystick)
            myJoystick.get_name()
            myJoystick.init()
            print(self.db.timeStr + ':\tSuccessfully connected to', pygame.joystick.Joystick(desiredJoystick).get_name(), '!')
        else:
            print(self.db.timeStr + ':\tFANATEC ClubSport Wheel Base not found!')

