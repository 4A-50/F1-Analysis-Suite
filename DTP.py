#<editor-fold desc="Imports">
import fastf1 as ff1
import pandas as pd
import datetime
import FLMS
from rich.console import Console
from rich.table import Table
from rich import box
from rich.style import Style
#</editor-fold>

#<editor-fold desc="Set Ups">
ff1.Cache.enable_cache('Cache/')
pd.options.mode.chained_assignment = None

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
    driverLaps = laps.pick_driver(driver).pick_wo_box()

    #Creates A Dataframe For The Drivers Lap Info
    lapInfo = pd.DataFrame(columns=['Lap', 'Stint', 'Compound', 'Life', 'Fresh', 'LapTime'])

    # Creates A Table To Output The Results
    outputTable = Table(title="Tyre Lap Info", box=box.SIMPLE, title_style=mainStyle)
    # Adds The Columns
    outputTable.add_column("Lap", justify="center")
    outputTable.add_column("Stint", justify="center")
    outputTable.add_column("Compound", justify="center")
    outputTable.add_column("Life", justify="center")
    outputTable.add_column("Fresh", justify="center")
    outputTable.add_column("Lap Time", justify="center")

    #Loops Through Every Lap In The Race
    for index, row in driverLaps.iterlaps():
        #Adds The Info To The DataFrame
        lapInfo = lapInfo.append({'Lap': row['LapNumber'], 'Stint': row['Stint'], 'Compound': row['Compound'], 'Life': row['TyreLife'], 'Fresh': row['FreshTyre'], 'LapTime': row['LapTime']}, ignore_index=True)

        #If Verbose Is Passed In
        if verbose:
            #Get The Tyres Colour
            colourCodedCompound = "[" + tyreColorCodes[row['Compound']] + "]" + row['Compound'] + "[/" + tyreColorCodes[row['Compound']] + "]"
            #Adds The Info To The Table
            outputTable.add_row(str(int(row['LapNumber'])), str(int(row['Stint'])), colourCodedCompound, str(row['TyreLife']), str(row['FreshTyre']), str(row['LapTime']))

    #If Verbose Is Passed In
    if verbose:
        #Print Out The Table
        console.print(outputTable)

def StintTyrePerformance(driver, year, race, session, stint, verbose):
    print("STP")