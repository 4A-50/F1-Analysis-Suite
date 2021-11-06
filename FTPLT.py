#<editor-fold desc="Imports">
import fastf1 as ff1
from fastf1 import plotting
import pandas as pd
import datetime
#</editor-fold>

#<editor-fold desc="Setups">
plotting.setup_mpl()
ff1.Cache.enable_cache('Cache/')
pd.options.mode.chained_assignment = None
#</editor-fold>

def FastestTechnicallyPossibleLapTime(driver, year, race, session, verbose):
    #Gets The Laps From The Inputted Race Info
    race = ff1.get_session(year, race, session)
    laps = race.load_laps(with_telemetry=True)

    #Pics The Laps From The Inputted Driver
    driverLaps = laps.pick_driver(driver)

    #Creates A Dataframe For The Drivers Lap Info
    telemetry = pd.DataFrame()
    #Loops Through Every Lap In The Race
    for lap in driverLaps.iterlaps():
        #Gets The Laps Distance
        driver_telemetry = lap[1].get_telemetry().add_distance()
        #Gets The Laps Number
        driver_telemetry['Lap'] = lap[1]['LapNumber']

        #Adds It To The Total Telemetry
        telemetry = telemetry.append(driver_telemetry)

    #The Amount Of MiniSectors
    numberOfMiniSectors = 25
    #The Laps Total Distance
    totalLapDistance = max(telemetry['Distance'])

    # Generate equally sized mini-sectors
    miniSectorLength = totalLapDistance / numberOfMiniSectors

    #Creates A MiniSector Array
    miniSectors = [0]

    #Loops Through All The MiniSectors
    for i in range(0, (numberOfMiniSectors - 1)):
        #Adds The Current MiniSector To The Array
        miniSectors.append(miniSectorLength * (i + 1))

        #Assign MiniSector To Every Row In The Telemetry Data
        telemetry['MiniSector'] = telemetry['Distance'].apply(lambda z: (miniSectors.index(min(miniSectors, key=lambda x: abs(x - z))) + 1))

    # Gets The Average Values
    average_speed = telemetry.groupby(['Lap', 'MiniSector'])['Speed'].mean().reset_index()
    average_gear = telemetry.groupby(['Lap', 'MiniSector'])['nGear'].mean().reset_index()
    # Adds The Gears Onto The Speed DataFrame
    average_speed['Gear'] = average_gear['nGear']
    # Renames The Var
    averageAllInfo = average_speed

    #Goes Through Every MiniSector Of Every Lap And Finds The Fastest For That MiniSector
    fastestMiniSectors = averageAllInfo.loc[averageAllInfo.groupby(['MiniSector'])['Speed'].idxmax()]

    #Creates A New TimeDelta To Hold The Lap Time
    fastestPosLapTime = datetime.timedelta()
    #Creates A New Array To Hold All Of The Laps Used In The Fastest Technically Possible Lap Time
    lapsUsed = []

    #Loops Through All Of The Fastest MiniSectors To Work Out Their Rough/Estimated Time (Distance / Speed)
    for index, row in fastestMiniSectors.iterrows():
        #Works Out The Time (Speed Is Divided By 3.6 To Convert From M/S To Km/H)
        estimatedTime = miniSectorLength / (row['Speed'] / 3.6)

        #Adds This MiniSectors Time To The Overall Laps Time
        fastestPosLapTime += datetime.timedelta(seconds=estimatedTime)

        #If The Lap This Was From Hasn't Already Been Added To The Array Add It
        if row['Lap'] not in lapsUsed:
            lapsUsed.append(row['Lap'])

        #If Verbose Was Passed In As A Parameter
        if verbose:
            #Prints Out Some More Detailed Info About Each MiniSector
            print("MiniSector " + str(row['MiniSector']) + " | Speed " + str(row['Speed']) + " | Time " + str(estimatedTime) + " | On Lap " + str(row['Lap']) + " | Gear " + str(row['Gear']))

    #Prints Out What The Fastest Technically Possible Lap Time Is
    print("Fastest Technically Possible Lap Time ~" + str(fastestPosLapTime))

    #The Driver Actual Fastest Lap
    driverActualFastestLap = driverLaps.pick_fastest()
    #Prints Out What The Fastest Lap Actually Was
    print("Actual Fastest Lap " + str(driverActualFastestLap['LapTime'].to_pytimedelta()) + " On Lap " + str(driverActualFastestLap['LapNumber']))

    #Prints Out What Laps Were Used To Make The Fastest Technically Possible Lap Time
    print("Fastest Technically Possible Time Made Up From MiniSectors On Laps:" + str(lapsUsed))

    #Prints Out The Time Differance Between The Two Laps
    print("Differance In Lap Times: " + str((driverActualFastestLap['LapTime'] - fastestPosLapTime).to_pytimedelta()))
