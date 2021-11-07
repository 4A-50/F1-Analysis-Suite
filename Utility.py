#<editor-fold desc="Imports">
import fastf1 as ff1
import pandas as pd
#</editor-fold>

#<editor-fold desc="Set Ups">
pd.options.mode.chained_assignment = None
#</editor-fold>

#An Array Of The Current Drivers (In DriverID Format Due To Driver Numbers Not Being Fixed Before 2014 & Due To Identifier Changes E.G. VES -> VER & To Avoid Family Relations E.G. Mick And Michael Schumacher Both Using MSC)
currentDrivers = ('hamilton', 'bottas', 'max_verstappen', 'perez', 'norris', 'ricciardo', 'vettel', 'stroll', 'ocon', 'alonso', 'sainz', 'leclerc', 'gasly', 'tsunoda', 'raikkonen', 'giovinazzi', 'mick_schumacher', 'mazepin', 'russell', 'latifi')

#A Dictionary Of Years And The Amount Of Races That Took Place
racesPerYear = {2021 : 17, 2020 : 17, 2019 : 21, 2018 : 21, 2017 : 20, 2016 : 21, 2015 : 19, 2014 : 19, 2013 : 19, 2012 : 20, 2011 : 19, 2010 : 19, 2009 : 17, 2008 : 18, 2007 : 17, 2006 : 18, 2005 : 19, 2004 : 18, 2003 : 16, 2002 : 17, 2001 : 17}

#A DataFrame To Hold The Info
qualiToRacePos = pd.DataFrame(columns=['Driver', 'QualiPos', 'RacePos', 'DNF'])

#Goes Through Every Race From The Array And Finds The Currently Active Drivers Start & Finish Pos
def FullCurrentDriverRaceHistory():
    #Shuts PyCharm Up
    global qualiToRacePos

    #Goes Through All The Years Backwards (E.G.2001 -> 2002 -> 2003)
    for y in reversed(racesPerYear):
        #Goes Through Each Race That Year (Amount Plus 1 Is Needed As Range In Inclusive)
        for i in range(1, racesPerYear[y] + 1):
            #Gets The Race
            race = ff1.get_session(y, i, 'R')
            #Gets The Results
            raceResults = race.results

            #Goes Through Every Driver In The Race
            for index in raceResults:
                #If They Are A Current Driver
                if index['Driver']['driverId'] in currentDrivers:
                    #Some Races Before 2004 If Räikkönen or Alonso Retired Crash The Get Driver Call. Try Then Stops The Program Crash
                    try:
                        #Gets The DNF Bool
                        dnfStatus = race.get_driver(index['Driver']['code']).dnf
                    except:
                        #If It Can't Get It Put Year And Race Number For Manual Entry
                        dnfStatus = str(y) + " " + str(i)

                    #Add The Info Tho The DataFrame
                    qualiToRacePos = qualiToRacePos.append({'Driver': index['Driver']['driverId'], 'QualiPos': index['grid'], 'RacePos': index['position'], 'DNF': dnfStatus}, ignore_index=True)

    #Saves The DataFrame To A CSV File
    qualiToRacePos.to_csv('QualiConversions.csv')

#Appends A Races Data To The End Of The CSV File
def AddRaceToHistory(raceYear, raceNumber):
    # Shuts PyCharm Up
    global qualiToRacePos

    #Loads The CSV File To Append To
    qualiToRacePos = pd.read_csv('QualiConversions.csv', index_col=0)

    #Gets The Race
    race = ff1.get_session(raceYear, raceNumber, 'R')
    #Gets The Results
    raceResults = race.results

    #Goes Through Every Driver In The Race
    for index in raceResults:
        #If They Are A Current Driver
        if index['Driver']['driverId'] in currentDrivers:
            #Add The Info Tho The DataFrame
            qualiToRacePos = qualiToRacePos.append({'Driver': index['Driver']['driverId'], 'QualiPos': index['grid'], 'RacePos': index['position'], 'DNF': race.get_driver(index['Driver']['code']).dnf}, ignore_index=True)

    #Saves The DataFrame To A CSV File
    qualiToRacePos.to_csv('QualiConversions.csv')


#FullCurrentDriverRaceHistory() Is Used To Start The CSV
#AddRaceToHistory(2021, 18) Is Used To Add A Races Data To The End