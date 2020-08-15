from functionalities.MultiSwitch import MultiSwitch
from functionalities.RTDB import RTDB

calcData = {'startUp': False,
            'LastFuelLevel': 0,
            'SessionInfoAvailable': False,
            'SessionNum': 0,
            'init': False,
            'BWasOnPitRoad': False,
            'BDDUexecuting': False,
            'WasOnTrack': False,
            'StintLap': 0,
            'oldSessionNum': -1,
            'oldLap': 0.1,
            'FuelConsumptionList': [],
            'FuelAvgConsumption': 0,
            'NLapRemaining': 0,
            'VFuelAdd': 0,
            'FuelLastCons': 0,
            'OutLap': True,
            'oldSessionlags': 0,
            'LapsToGo': 27,
            'Run': 0,
            'SessionLapRemain': 0,
            'FuelConsumptionStr': '6.35',
            'RemLapValueStr': '9.3',
            'FuelLapStr': '6.3',
            'FuelAddStr': '23.6',
            'ToGoStr': '102/256',
            'FlagCallTime': 0,
            'FlagException': False,
            'FlagExceptionVal': 0,
            'Alarm': [0]*10,
            'VFuelAddOld': 1,
            'GreenTime': 0,
            'RemTimeValue': 0,
            'RaceLaps': 37,
            'JokerStr': '2/2',
            'dist': [],
            'x': [],
            'y': [],
            'map': [],
            'RX': False,
            'BCreateTrack': True,
            'dx': [],
            'dy': [],
            'logLap': 0,
            'Logging': False,
            'tempdist': -1,
            'StartUp': False,
            'oldSessionFlags': 0,
            'backgroundColour': (0, 0, 0),
            'textColourFuelAdd': (255, 255, 255),
            'textColourFuelAddOverride': (255, 255, 255),
            'BTextColourFuelAddOverride': False,
            'textColour': (255, 255, 255),
            'FuelLaps': 1,
            'FuelAdd': 1,
            'PitStopDelta': 61,
            'time': [],
            'UpshiftStrategy': 0,
            'UserShiftRPM': [100000, 100000, 100000, 100000, 100000, 100000, 100000],
            'UserShiftFlag': [1, 1, 1, 1, 1, 1, 1],
            'iRShiftRPM': [100000, 100000, 100000, 100000],
            'ShiftToneEnabled': True,
            'StartDDU': False,
            'StopDDU': False,
            'DDUrunning': False,
            'UserRaceLaps': 0,
            'SessionLength': 86400,
            'CarIdxPitStops': [0] * 64,
            'CarIdxOnPitRoadOld': [True] * 64,
            'PitStopsRequired': 0,
            'old_DRS_Status': 0,
            'DRSActivations': 8,
            'P2PActivations': 12,
            'DRSActivationsGUI': 8,
            'P2PActivationsGUI': 12,
            'JokerLapDelta': 2,
            'JokerLaps': 1,
            'MapHighlight': False,
            'old_PushToPass': False,
            'textColourDRS': (255, 255, 255),
            'textColourP2P': (255, 255, 255),
            'textColourJoker': (255, 255, 255),
            'DRSCounter': 0,
            'P2PCounter': 0,
            'P2PStr': '12',
            'DRSStr': '12',
            'RenderLabel': [
                True,  # 0 Best
                True,  # 1 Last
                True,  # 2 Delta
                True,  # 3 FuelLevel
                True,  # 4 FuelCons
                True,  # 5 FuelLastCons
                True,  # 6 FuelLaps
                True,  # 7 FuelAdd
                True,  # 8 ABS
                True,  # 9 BBias
                True,  # 10 Mix
                True,  # 11 TC1
                True,  # 12 TC2
                True,  # 13Lap
                True,  # 14 Clock
                True,  # 15 Remain
                False,  # 16 Elapsed
                True,  # 17 Joker
                False,  # 18 DRS
                False,  # 19 P2P
                True,  # 20 ToGo
                True,  # 21 Est
                True,  # 22 Gear
                True,  # 23 Speed
                True,  # 24 Position
                True,  # 25 Distance to pit stall
                True,  # 26 speed in pit lane
                True,  # 27 Gear in pit lane
            ],
            'P2P': False,
            'DRS': False,
            'LapLimit': False,
            'TimeLimit': False,
            'P2PTime': 0,
            'DRSRemaining': 0,
            'dcFuelMixtureOld': 0,
            'dcThrottleShapeOld': 0,
            'dcTractionControlOld': 0,
            'dcTractionControl2Old': 0,
            'dcTractionControl': 0,
            'dcTractionControl2': 0,
            'dcTractionControlToggleOld': 0,
            'dcABSOld': 0,
            'dcBrakeBiasOld': 0,
            'dcBrakeBias': 0,
            'RunStartTime': 0,
            'changeLabelsOn': True,
            'dcChangeTime': 0,
            'dcFuelMixtureChange': False,
            'dcThrottleShapeChange': False,
            'dcTractionControlChange': False,
            'dcTractionControl2Change': False,
            'dcTractionControlToggleChange': False,
            'dcABSChange': False,
            'dcBrakeBiasChange': False,
            'BUpshiftToneInitRequest': False,
            'BNewLap': False,
            'NLapDriver': 0,
            'NLapRaceTime': [0] * 64,
            'TFinishPredicted': [0] * 64,
            'WinnerCarIdx': 0,
            'DriverCarIdx': 0,
            'NLapWinnerRaceTime': 0,
            'PosStr': '64/64',
            'SpeedStr': '234',
            'GearStr': 'N',
            'classStruct': {},
            'NClasses': 1,
            'NDrivers': 1,
            'NDriversMyClass': 1,
            'SOF': 0,
            'SOFMyClass': 0,
            'NClassPosition': 1,
            'NPosition': 1,
            'BResults': False,
            'aOffsetTrack': 0,
            'weatherStr': 'TAir: 25°C     TTrack: 40°C     pAir: 1.01 bar    rHum: 50 %     rhoAir: 1.25 kg/m³     vWind: ',
            'SOFstr': 'SOF: 0',
            'BdcHeadlightFlash': False,
            'tdcHeadlightFlash': 0,
            'dcHeadlightFlashOld': False,
            'newLapTime': 0,
            'BEnableRaceLapEstimation': False,
            'track': None,
            'car': None,
            'SubSessionIDOld': 0,
            'NDDUPage': 1,
            'dc': {'dcABS',
                   'dcTractionControl',
                   'dcTractionControl2',
                   'dcBrakeBias'
                   },
            'dcOld': {},
            'dcChangedItems': {},
            'BLoggerActive': False,
            'tExecuteRTDB': 0,
            'tExecuteUpshiftTone': 0,
            'tExecuteRaceLapsEstimation': 0,
            'tExecuteLogger': 0,
            'tExecuteRender': 0,
            'tExecuteCalc': 0,
            'tShiftReaction': float('nan'),
            'BEnableLapLogging': False,
            'BChangeTyres': False,
            'BBeginFueling': False,
            'VUserFuelSet': 0,
            'NFuelSetMethod': 0, # 0 = User pre set; 1 = calculated
            'BPitCommandUpdate': False,
            'PlayerTrackSurfaceOld': 0,
            'BEnteringPits': False,
            'BPitCommandControl': False,
            'sToPitStall': 0,
            'sToPitStallStr': '463',
            'PitSvFlagsEntry': 0,
            'BFuelRequest': False,
            'BFuelCompleted': False,
            'BTyreChangeRequest': [False, False, False, False],
            'BTyreChangeCompleted':  [False, False, False, False],
            'VFuelPitStopStart': 0,
            'BPitstop': False,
            'BPitstopCompleted': False,
            'NLappingCars': [
                {
                'Class': 'LMP1',
                'NCars': 2,
                'Color': (255, 218, 89),
                'sDiff': -10
                },
                {
                'Class': 'HPD',
                'NCars': 1,
                'Color': (255, 218, 89),
                'sDiff': -50
                }
            ],
            'PlayerCarClassRelSpeed': 0,
            'Exception': None,
            'BLiftToneRequest': False,
            'FuelTGTLiftPoints': {},
            'VFuelTgt': 3.05,
            'VFuelTgtEffective': 3.05,
            'VFuelTgtOffset': 0,
            'BLiftBeepPlayed': [],
            'NNextLiftPoint': 0,
            'BEnableLiftTones': False,
            'tNextLiftPoint': 0,
            'DDUControlList':
                {
                'VFuelTgt': ['VFuelTgt', True, 2],
                'VFuelTgtOffset': ['VFuelTgtOffset', True, 2]
                },
            'fFuelBeep': 300,
            'tFuelBeep': 150,
            'fShiftBeep': 500,
            'tShiftBeep': 150,
            'dcABS': 6,
            'NButtonPressed': None,
            'NCurrentMap': 0
            }

myRTDB = RTDB.RTDB()
myRTDB.initialise(calcData, False)

ms = MultiSwitch.MultiSwitch(myRTDB, 0.01)

ms.addMapping('BEnableLiftTones')
ms.addMapping('BBeginFueling')
ms.addMapping('LapsToGo', minValue=0, maxValue=100, step=5)
ms.addMapping('dcABS', minValue=0, maxValue=12, step=1)
ms.addMapping('dcTractionControl', minValue=0, maxValue=12, step=1)
ms.addMapping('dcTractionControl2', minValue=0, maxValue=12, step=1)
ms.addMapping('dcBrakeBias', minValue=0, maxValue=12, step=1)

# print(ms.db.__getattribute__('LapsToGo'))
#
# ms.maps['LapsToGo'].decrease()
#
# print(ms.db.__getattribute__('LapsToGo'))
#
#
# ms.maps['dcABS'].decrease()
#
# ms.maps['dcABS'].increase()

ms.run()



# m1 = MultiSwitch.MultiSwitchItem()
#
# m2 = MultiSwitch.MultiSwitchItem()
#
# m3 = MultiSwitch.MultiSwitchItem()
#
#
# print(m1.db)
# print(m2.db)
# print(m3.db)
#
#
# m3.db = 123
#
# MultiSwitch.MultiSwitchItem.db = 4
# m4 = MultiSwitch.MultiSwitchItem()
#
#
# print(m1.db)
# print(m2.db)
# print(m3.db)
# print(m4.db)