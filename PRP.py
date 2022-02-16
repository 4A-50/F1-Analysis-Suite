#<editor-fold desc="Imports">
import fastf1 as ff1
import pandas as pd

from rich.console import Console
from rich.table import Table
from rich import box
from rich.style import Style
#</editor-fold>

#<editor-fold desc="Set Ups">
pd.options.mode.chained_assignment = None

console = Console(highlight = False)
mainStyle = Style(color = "yellow")
errorStyle = Style(color = "red")
#</editor-fold>

#Loads The CSV File
qualiToRacePos = pd.read_csv('QualiConversions.csv', index_col=0)



def PredictedRacePosition(driver, startingPos, verbose):
    #Gets A Race With All Current Drivers In To Get Their Data From (Use First Race Of Current Year)
    driverInfo = ff1.get_session(2021,1,'R').get_driver(driver)
    #Gets The Inputted Drivers DriverID
    driverID = driverInfo.info['Driver']['driverId']

    #Gets ALl The Drivers Quali To Race Positions
    allDriversQTRPs = qualiToRacePos[qualiToRacePos['Driver'] == driverID]
    #Gets All The Ones The Driver Didn't DNF
    allDriversQTRPsNDNF = allDriversQTRPs[allDriversQTRPs['DNF'] == False]
    #Gets All The Ones From The Inputted Start Pos
    currentStartPosQTRPs = allDriversQTRPsNDNF[allDriversQTRPsNDNF['QualiPos'] == startingPos]

    # If Verbose Was Passed In As A Parameter
    if verbose:
        # Creates A Table To Output The Results
        outputTable = Table(title="Race Start To Race End Positions", box=box.SIMPLE, title_style=mainStyle)
        # Adds The Columns
        outputTable.add_column("Start Pos", justify="center", style=mainStyle)
        outputTable.add_column("End Pos", justify="center")

    #Creates A Dictionary Of All The Race End Positions With Count Of How Many Time They Were Achieved
    racePosDict = {i:(currentStartPosQTRPs['RacePos'].tolist()).count(i) for i in (currentStartPosQTRPs['RacePos'].tolist())}

    #If Verbose Was Passed In As A Parameter
    if verbose:
        #Loops Through All The Rows
        for index, row in currentStartPosQTRPs.iterrows():
            #If They Finished Lower Than They Started
            if row['QualiPos'] >= row['RacePos']:
                #Prints The Race Pos In Green
                finalPosOutput = "[green]" + str(row['RacePos']) + "[/green]"
            else:
                #Prints The Race Pos In Red
                finalPosOutput = "[red]" + str(row['RacePos']) + "[/red]"

            #Adds The Row To The Table
            outputTable.add_row(str(row['QualiPos']), finalPosOutput)

    #If Verbose Was Passed In As A Parameter
    if verbose:
        #Outputs The Table
        console.print(outputTable)

    #If The Driver Has Qualified Their Before
    if len(racePosDict) > 0:
        #Gets The Key Of The Largest Value
        mostCommonEndPos = max(racePosDict, key=racePosDict.get)
        #Works Out The Percentage Of Finishing There
        mostCommonEndPosPercentage = round((racePosDict[mostCommonEndPos] / len(currentStartPosQTRPs['RacePos'])) * 100)

        #Outputs The Data
        console.print("Most Likely Finishing Place Is [yellow]" + str(mostCommonEndPos) + ".[/yellow]")
        console.print("With A [yellow]" + str(mostCommonEndPosPercentage) + "%[/yellow] Chance.")

        #Prints A Warning If The Data Set Is Small
        if len(currentStartPosQTRPs) <= 5:
            console.print("This Is A Small Data Set, Outcome Prediction Isn't Very Accurate.", style=errorStyle)
    else:
        #Prints That The Driver Hasn't Qualified There Before
        console.print("This Driver Hasn't Qualified In This Position Before, Can't Predict Outcome!", style=errorStyle)