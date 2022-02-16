#<editor-fold desc="Imports">
import fastf1 as ff1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from rich.console import Console
from rich.table import Table
from rich import box
from rich.style import Style
#</editor-fold>

#<editor-fold desc="Set Ups">
ff1.Cache.enable_cache('Cache/')
pd.options.mode.chained_assignment = None
fastf1.plotting.setup_mpl()

console = Console(highlight = False)
mainStyle = Style(color = "yellow")
#</editor-fold>

#Colour Codes For The Tyres
tyreColorCodes = {"SOFT": 'red', "MEDIUM": 'yellow', "HARD": 'white', "INTERMEDIATE": 'green', "WET": 'blue'}

def AllStintsTyrePerformance(driver, year, race, session, verbose):
    #Gets The Laps From The Inputted Race Info
    F1Session = ff1.get_session(year, race, session)
    laps = F1Session.load_laps(with_telemetry=True)

    #Picks The Accurate Laps That Aren't In Or Out Laps From The Inputted Driver
    driverLaps = laps.pick_wo_box()

    #Creates A Dataframe For The Drivers Lap Info
    lapInfo = pd.DataFrame(columns=['Lap', 'Stint', 'Compound', 'Life', 'Fresh', 'LapTime'])

    fastestTimePerLap = {}
    fastestDriverPerLap = {}

    # Creates A Table To Output The Results
    outputTable = Table(title="Tyre Lap Info", box=box.SIMPLE, title_style=mainStyle)
    # Adds The Columns
    outputTable.add_column("Lap", justify="center")
    outputTable.add_column("Stint", justify="center")
    outputTable.add_column("Compound", justify="center")
    outputTable.add_column("Life", justify="center")
    outputTable.add_column("Fresh", justify="center")
    outputTable.add_column("Lap Time", justify="center")
    outputTable.add_column("Delta", justify="center")

    #If Verbose Was Passed In As A Parameter
    if verbose:
        outputTable.add_column("Fast Lap Time", justify="center")
        outputTable.add_column("Fast Lap Driver", justify="center")

        #Creates The Graph Info
        fig, ax = plt.subplots()
        graphInfo = pd.DataFrame(columns=['Lap', 'Driver', 'FastestLap'])

    #Loops Through Every Lap In The Race
    for index, row in driverLaps.iterlaps():
        if row['Driver'] == driver:
            #Adds The Info To The DataFrame
            lapInfo = lapInfo.append({'Lap': row['LapNumber'], 'Stint': row['Stint'], 'Compound': row['Compound'], 'Life': row['TyreLife'], 'Fresh': row['FreshTyre'], 'LapTime': row['LapTime']}, ignore_index=True)
        else:
            if row['LapNumber'] not in fastestTimePerLap:
                fastestTimePerLap[row['LapNumber']] = row['LapTime']
                fastestDriverPerLap[row['LapNumber']] = row['Driver']
            else:
                if row['LapTime'] < fastestTimePerLap[row['LapNumber']]:
                    fastestTimePerLap[row['LapNumber']] = row['LapTime']
                    fastestDriverPerLap[row['LapNumber']] = row['Driver']


    #Add's The Fastest Lap Times To The Table
    for index, row in lapInfo.iterrows():
        #Get The Tyres Colour
        colourCodedCompound = "[" + tyreColorCodes[row['Compound']] + "]" + row['Compound'] + "[/" + tyreColorCodes[row['Compound']] + "]"

        #Re-Configures The Lap Time
        driverLapTime = datetime.timedelta(seconds=row['LapTime'].seconds, microseconds=row['LapTime'].microseconds)

        #Re-Configures The Fastest Lap Time
        fastestLapTime = datetime.timedelta(seconds=fastestTimePerLap[row['Lap']].seconds, microseconds=fastestTimePerLap[row['Lap']].microseconds)

        #Colours The Lap Delta
        if driverLapTime < fastestLapTime:
            colouredDelta = "[green]" + str(fastestLapTime - driverLapTime) + "[/green]"
        else:
            colouredDelta = "[red]" + str(driverLapTime - fastestLapTime) + "[/red]"

        #If Verbose Was Passed In As A Parameter
        if verbose:
            #Adds The Info To The Table
            outputTable.add_row(str(int(row['Lap'])), str(int(row['Stint'])), colourCodedCompound, str(row['Life']), str(row['Fresh']), str(driverLapTime), colouredDelta, str(fastestLapTime), fastestDriverPerLap[row['Lap']])

            graphInfo = graphInfo.append({'Lap': row['Lap'], 'Driver': driverLapTime, 'FastestLap': fastestLapTime}, ignore_index=True)
        else:
            # Adds The Info To The Table
            outputTable.add_row(str(int(row['Lap'])), str(int(row['Stint'])), colourCodedCompound, str(row['Life']), str(row['Fresh']), str(driverLapTime), colouredDelta)

    #Print Out The Table
    console.print(outputTable)

    # If Verbose Was Passed In As A Parameter
    if verbose:
        ax.plot(graphInfo['Lap'], graphInfo['Driver'], label = driver)
        ax.plot(graphInfo['Lap'], graphInfo['FastestLap'], label = 'Fastest Time')

        ax.set_xlabel("Lap Number")
        ax.set_ylabel("Lap Time")

        ax.legend()
        plt.suptitle("Driver Tyre Performance Delta \n" + F1Session.weekend.name + " " + str(F1Session.weekend.year))
        plt.show()