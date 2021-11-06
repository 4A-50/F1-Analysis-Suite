#<editor-fold desc="Imports">
import fastf1 as ff1
from fastf1 import plotting
import pandas as pd
import datetime
import FLMS
from rich.console import Console
from rich.table import Table
from rich import box
from rich.style import Style
#</editor-fold>

#<editor-fold desc="Setups">
plotting.setup_mpl()
ff1.Cache.enable_cache('Cache/')
pd.options.mode.chained_assignment = None

console = Console(highlight = False)
mainStyle = Style(color = "yellow")
#</editor-fold>

def FastestTechnicallyPossibleLapTime(driver, year, race, session, msCount, verbose):
    #Gets The Laps From The Inputted Race Info
    F1Session = ff1.get_session(year, race, session)
    laps = F1Session.load_laps(with_telemetry=True)

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

    #Sets The Amount Of MiniSectors
    if msCount is None:
        #The Default Is 25
        numberOfMiniSectors = 25
    else:
        numberOfMiniSectors = msCount

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
    #Creates A New Array To Hold The MiniSector Times
    FMSTimes = []

    #If Verbose Was Passed In As A Parameter
    if verbose:
        #Creates A Table To Output The Results
        FTPMSTable = Table(title = "Fastest Technically Possible MiniSectors", box = box.SIMPLE, title_style = mainStyle)
        #Adds The Columns
        FTPMSTable.add_column("MiniSector", justify = "center")
        FTPMSTable.add_column("Speed", justify = "center")
        FTPMSTable.add_column("Gear", justify = "center")
        FTPMSTable.add_column("~Time", justify = "center")
        FTPMSTable.add_column("Lap", justify = "center")

    #Loops Through All Of The Fastest MiniSectors To Work Out Their Rough/Estimated Time (Distance / Speed)
    for index, row in fastestMiniSectors.iterrows():
        #Works Out The Time (Speed Is Divided By 3.6 To Convert From M/S To Km/H)
        estimatedTime = miniSectorLength / (row['Speed'] / 3.6)

        #Adds This MiniSectors Time To The Overall Laps Time
        fastestPosLapTime += datetime.timedelta(seconds=estimatedTime)

        #Adds This MiniSectors Time To The Array
        FMSTimes.append(datetime.timedelta(seconds=estimatedTime))

        #If The Lap This Was From Hasn't Already Been Added To The Array Add It
        if row['Lap'] not in lapsUsed:
            lapsUsed.append(row['Lap'])

        #If Verbose Was Passed In As A Parameter
        if verbose:
            #Adds Some More Detailed Info About Each MiniSector To The Table
            FTPMSTable.add_row(str(int(row['MiniSector'])), str(row['Speed']), str(row['Gear']), str(estimatedTime), str(int(row['Lap'])))

    #If Verbose Was Passed In As A Parameter
    if verbose:
    #Prints Out The FTPMSTable
        console.print(FTPMSTable)

    #Prints Out What The Fastest Technically Possible Lap Time Is
    console.print("Fastest Technically Possible Lap Time ~" + str(fastestPosLapTime), style = mainStyle)

    #The Driver Actual Fastest Lap
    driverActualFastestLap = driverLaps.pick_fastest()
    #Prints Out What The Fastest Lap Actually Was
    console.print("Actual Fastest Lap " + str(driverActualFastestLap['LapTime'].to_pytimedelta()) + " On Lap " + str(driverActualFastestLap['LapNumber']), style = mainStyle)

    #Prints Out What Laps Were Used To Make The Fastest Technically Possible Lap Time
    console.print("Fastest Technically Possible Time Made Up From MiniSectors On Laps: " + str(lapsUsed), style = mainStyle)

    #Prints Out The Time Differance Between The Two Laps
    console.print("Differance In Lap Times: [red]" + str((driverActualFastestLap['LapTime'] - fastestPosLapTime).to_pytimedelta()) + "[/red]", style = mainStyle)

    #If Verbose Is Passes In
    if verbose:
        #Gets The Drives Fastest Lap MiniSectors TODO This Seems Cumbersome Try And Redo This
        fastestLapMiniSectors = FLMS.FastestLapMiniSectors(driver, year, race, session, msCount, True)

        #Creates A Table To Output The Results
        lapTimeTable = Table(title = "Actual Fastest Lap Vs Fastest Technically Possible Lap", box = box.SIMPLE, title_style = mainStyle)
        #Adds The Columns
        lapTimeTable.add_column("MiniSector", justify="center")
        lapTimeTable.add_column("Gain/Loss", justify="center")
        lapTimeTable.add_column("Time Differance", justify="center")

        # Loops Through All Of The MiniSectors To Work Out Their Rough/Estimated Time (Distance / Speed)
        for index, row in fastestLapMiniSectors.iterrows():
            # Works Out The Time (Speed Is Divided By 3.6 To Convert From M/S To Km/H)
            estimatedTime = miniSectorLength / (row['Speed'] / 3.6)
            #The Time Value Of This MiniSector
            fastestLapMSTime = datetime.timedelta(seconds = estimatedTime)

            if fastestLapMSTime > FMSTimes[int(row['MiniSector']) - 1]:
                lapTimeTable.add_row(str(int(row['MiniSector'])), "Lost", "[red]" + str(fastestLapMSTime - FMSTimes[int(row['MiniSector']) - 1]) + "[/red]")
            else:
                lapTimeTable.add_row(str(int(row['MiniSector'])), "Gained", "[green]" + str(FMSTimes[int(row['MiniSector']) - 1] - fastestLapMSTime) + "[/green]")

        console.print(lapTimeTable)