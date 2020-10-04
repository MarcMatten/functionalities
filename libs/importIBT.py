import irsdk
import numpy as np
import scipy.signal
from functionalities.libs import importExport

# TODO: better logging

def importIBT(ibtPath, channels=None, lap=None, channelMapPath='iRacingChannelMap.csv'):

    # read in telemetry channels
    ir_ibt = irsdk.IBT()
    ir_ibt.open(ibtPath)
    var_headers_names = ir_ibt.var_headers_names

    temp = dict()
    s = dict()

    # load channel map
    channelMap = importExport.loadCSV(channelMapPath)

    # define telemetry channels to import
    channelsExport= []

    if channels is None:
        channelsExport = var_headers_names
    else:
        for i in range(0, len(channels)):
            if channels[i] in var_headers_names:
                channelsExport.append(channels[i])
            elif channels[i] in channelMap['ChannelName']:
                index = channelMap['ChannelName'].index(channels[i])
                channelsExport.append(channelMap['iRacingChannelName'][index])
            else:
                print('Error: <{}> neihter in list of iRacing channels nor in channel map! - Skipping this channel!'.format(channels[i]))

    channelsExport.extend(['LapCurrentLapTime', 'LapDist', 'Speed', 'Lap'])
    channelsExport = list(set(channelsExport))

    # import channels
    for i in range(0, len(channelsExport)):
        if channelsExport[i] in var_headers_names:
            temp[channelsExport[i]] = np.array(ir_ibt.get_all(channelsExport[i]))
        else:
            print('Error: <{}> not in the list of available channels'.format(channelsExport[i]))

    varNames = list(temp.keys())

    # cut data
    if lap is None or lap in ['a', 'A', 'all', 'ALL', 'All', 'w', 'W', 'whole', 'WHOLE']:  # complete file
        for i in range(0, len(varNames)):
            s[varNames[i]] = temp[varNames[i]]
    else:
        indices = []
        if lap in ['f', 'F', 'fastest', 'Fastest', 'FASTERST']:  # fastest lap only
            # find the fastest lap
            NLapStartIndex = scipy.signal.find_peaks(1 - np.array(temp['LapDistPct']), height=(0.98, 1.02))

            tLap = []
            NLap = []
            for q in range(0, len(NLapStartIndex[0])-1):
                tLap.append(temp['SessionTime'][NLapStartIndex[0][q+1]-1] - temp['SessionTime'][NLapStartIndex[0][q]])
                NLap.append(temp['Lap'][NLapStartIndex[0][q]])

            NLapFastest = NLap[np.argmin(tLap)]

            # get all indices for the fastest lap
            indices = np.argwhere(temp['Lap'] == NLapFastest)[:, 0]

        # lap number
        elif isinstance(lap, int):
            if lap < np.min(temp['Lap']) or lap > np.max(np.array(temp['Lap'])):
                print('Error: Lap number {} is out of bounds! File contains laps {} to {}'.format(lap, np.min(temp['Lap']), np.max(np.array(temp['Lap']))))
                return

            indices = np.argwhere(temp['Lap'] == lap)[:, 0]

        # actually cut the data
        for i in range(0, len(varNames)):
            s[varNames[i]] = temp[varNames[i]][indices]

    ir_ibt.close()

    # channel mapping
    c = dict()

    for i in range(0, len(channelsExport)):
        if channelsExport[i] in channelMap['iRacingChannelName']:
            index = channelMap['iRacingChannelName'].index(channelsExport[i])
            c[channelMap['ChannelName'][index]] = np.array(s[channelsExport[i]]) * float(channelMap['ConverstionFactor'][index])
        else:
            c[channelsExport[i]] = s[channelsExport[i]]

    # read in metadata
    ir = irsdk.IRSDK()
    ir.startup(test_file=ibtPath)

    c['CarSetup'] = ir['CarSetup']
    c['DriverInfo'] = ir['DriverInfo']
    c['WeekendInfo'] = ir['WeekendInfo']

    ir.shutdown()

    return c, var_headers_names
