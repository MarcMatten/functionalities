import irsdk
import numpy as np
import matplotlib.pyplot as plt
import scipy. signal

# S = importIBT(MyIbtPath, MyChannelMap, 'f')
# MyIbtPath = 'C:/Users/Marc/Documents/iRacing/Telemetry/fordgt2017_monza full 2020-05-14 20-55-54.ibt'
#
channelMap = {'Speed': ['vCar', 1],  # m/s
                'LapCurrentLapTime': ['tLap', 1],  # s
                'LatAccel': ['gLat', 1],  # m/s²
                'LongAccel': ['gLong', 1],  # m/s²
                'ThrottleRaw': ['rThrottle', 1],  # 1
                'BrakeRaw': ['rBrake', 1],  # 1
                'FuelUsePerHour': ['QFuel', 1 / 3.6],  # l/h --> g/s
                'LapDist': ['sLap', 1],  # m
                'Alt': ['GPSAltitude', 1]  # m,
                }

def importIBT(ibtPath, *args):

    ir_ibt = irsdk.IBT()
    ir_ibt.open(ibtPath)
    temp = dict()
    s = dict()

    if len(args) > 1:
        print('Error: maximum 3 arguments can be supplied: file path, channel map and export criteria (lap number of f for fastest lap)!')
        return

    # import all
    for i in range(0, len(ir_ibt.var_headers_names)):
        if ir_ibt.var_headers_names[i] in channelMap:
            temp[channelMap[ir_ibt.var_headers_names[i]][0]] = np.array(ir_ibt.get_all(ir_ibt.var_headers_names[i])) * channelMap[ir_ibt.var_headers_names[i]][1]
        else:
            temp[ir_ibt.var_headers_names[i]] = np.array(ir_ibt.get_all(ir_ibt.var_headers_names[i]))

    varNames = list(temp.keys())

    # cut file as requested
    if len(args) == 1:
        if args[0] == 'f' or args[0] == 'F' or args[0] == 'fastest' or args[0] == 'Fastest':
            NLapTimesIndex = scipy.signal.find_peaks(np.array(temp['tLap']), prominence=10)
            NLapTimeFastestIndex = np.argmin(np.array(temp['tLap'])[NLapTimesIndex[0]])
            NLapFastest = temp['Lap'][NLapTimesIndex[0][NLapTimeFastestIndex]]

            indices = np.argwhere(temp['Lap'] == NLapFastest)[:, 0]

            for i in range(0, len(varNames)):
                if varNames[i] in channelMap:
                    s[channelMap[varNames[i]][0]] = temp[varNames[i]][indices]
                else:
                    s[varNames[i]] = temp[varNames[i]][indices]

        elif np.isint(args[0]):
            if args[0] < np.min(temp['Lap']) or args[0] > np.max(np.array(temp['Lap'])):
                print('Error: Lap out of bounds! File contains laps ' + str(np.min(temp['Lap'])) + ' to ' + str(np.max(np.array(temp['Lap']))))
                return

            indices = np.argwhere(temp['Lap'] == args[0])[:, 0]

            for i in range(0, len(varNames)):
                if varNames[i] in channelMap:
                    s[channelMap[varNames[i]][0]] = temp[varNames[i]][indices]
                else:
                    s[varNames[i]] = temp[varNames[i]][indices]

    else:  # complete file
        for i in range(0, len(varNames)):
            if varNames[i] in channelMap:
                s[channelMap[varNames[i]][0]] = temp[varNames[i]]
            else:
                s[varNames[i]] = temp[varNames[i]]

    ir_ibt.close()

    return s
