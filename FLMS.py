#<editor-fold desc="Imports">
import fastf1 as ff1
from fastf1 import plotting
import pandas as pd
import datetime
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

def FastestLapMiniSectors(driver, year, race, session, msCount, verbose, returnMode = False):
    #Gets The Laps From The Inputted Race Info
    race = ff1.get_session(year, race, session)
    laps = race.load_laps(with_telemetry=True)

    #Pics The Laps From The Inputted Driver
    driverFastestLap = laps.pick_driver(driver).pick_fastest()

    #Creates A Dataframe For The Drivers Lap Info
    telemetry = pd.DataFrame()
    #Gets The Laps Distance
    driver_telemetry = driverFastestLap.get_telemetry().add_distance()
    #Gets The Laps Number
    driver_telemetry['Lap'] = driverFastestLap['LapNumber']

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

    # Creates A Table To Output The Results
    FLMSTable = Table(title="Fastest Lap MiniSectors", box=box.SIMPLE, title_style=mainStyle)
    # Adds The Columns
    FLMSTable.add_column("MiniSector", justify="center")
    FLMSTable.add_column("Speed", justify="center")
    FLMSTable.add_column("Gear", justify="center")
    FLMSTable.add_column("~Time", justify="center")
    FLMSTable.add_column("Lap", justify="center")

    #Loops Through All Of The Fastest MiniSectors To Work Out Their Rough/Estimated Time (Distance / Speed)
    for index, row in fastestMiniSectors.iterrows():
        #Works Out The Time (Speed Is Divided By 3.6 To Convert From M/S To Km/H)
        estimatedTime = miniSectorLength / (row['Speed'] / 3.6)

        #Adds This MiniSectors Time To The Overall Laps Time
        fastestPosLapTime += datetime.timedelta(seconds=estimatedTime)

        #If The Lap This Was From Hasn't Already Been Added To The Array Add It
        if row['Lap'] not in lapsUsed:
            lapsUsed.append(row['Lap'])

        #Prints Out Some More Detailed Info About Each MiniSector
        FLMSTable.add_row(str(int(row['MiniSector'])), str(row['Speed']), str(row['Gear']), str(estimatedTime), str(int(row['Lap'])))

    if not returnMode:
        console.print(FLMSTable)
    else:
        return averageAllInfo