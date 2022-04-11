#<editor-fold desc="Imports">
import fastf1 as ff1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
#</editor-fold>

#<editor-fold desc="Set Ups">
ff1.Cache.enable_cache('Cache/')
pd.options.mode.chained_assignment = None
fastf1.plotting.setup_mpl()

plotSize = [15,15]
plotRatios = [3, 2, 1, 1, 2, 1]
#</editor-fold>

def DriverLapTelemetry(driver, year, race, session, lap, verbose):
    #Gets The Laps From The Inputted Race Info
    F1Session = ff1.get_session(year, race, session)
    laps = F1Session.load_laps(with_telemetry=True)

    #Finds The Specified Drivers Laps
    driverLaps = laps.pick_driver(driver)

    #Gets The Driver Fact Data (Team, Number Etc)
    driverInfo = F1Session.get_driver(driver)

    #Drivers Telemetry Data
    driverTel = pd.DataFrame()

    # Loops Through Every Lap In The Race To Find The Inputted One
    for index, row in driverLaps.iterlaps():
        if str(int(row['LapNumber'])) == lap:
            driverTel = row.get_telemetry().add_distance()

    #Increase The Plot Size
    plt.rcParams['figure.figsize'] = plotSize

    #Creates The Plot
    fig, ax = plt.subplots(6, gridspec_kw = {'height_ratios': plotRatios}, sharex = True)

    #Sets The Plots Title
    ax[0].title.set_text("Lap " + lap + " Telemetry For " + driver + "\n" + F1Session.weekend.name + " " + str(F1Session.weekend.year))

    #Plots
    ax[0].plot(driverTel['Distance'], driverTel['Speed'], color = fastf1.plotting.team_color(driverInfo.team), label = driver)
    ax[0].set(ylabel='Speed')

    ax[1].plot(driverTel['Distance'], driverTel['Throttle'], color = fastf1.plotting.team_color(driverInfo.team), label = driver)
    ax[1].set(ylabel='Throttle')

    ax[2].plot(driverTel['Distance'], driverTel['Brake'], color = fastf1.plotting.team_color(driverInfo.team), label = driver)
    ax[2].set(ylabel='Brake')

    ax[3].plot(driverTel['Distance'], driverTel['nGear'], color=fastf1.plotting.team_color(driverInfo.team), label=driver)
    ax[3].set(ylabel='Gear')

    ax[4].plot(driverTel['Distance'], driverTel['RPM'], color=fastf1.plotting.team_color(driverInfo.team), label=driver)
    ax[4].set(ylabel='RPM')

    ax[5].plot(driverTel['Distance'], driverTel['DRS'], color=fastf1.plotting.team_color(driverInfo.team), label=driver)
    ax[5].set(ylabel='DRS')
    ax[5].set(xlabel='Distance In Meters')

    #Cleans Up The Tick Labels
    for a in ax:
        a.label_outer()

    #Outputs The Plot
    plt.show()

def TwoDriverLapTelemetry(driver1, driver2, year, race, session, lap, verbose):
    # Gets The Laps From The Inputted Race Info
    F1Session = ff1.get_session(year, race, session)
    laps = F1Session.load_laps(with_telemetry=True)

    # Finds The Specified Drivers Laps
    driver1Laps = laps.pick_driver(driver1)
    driver2Laps = laps.pick_driver(driver2)

    # Gets The Driver Fact Data (Team, Number Etc)
    driver1Info = F1Session.get_driver(driver1)
    driver2Info = F1Session.get_driver(driver2)

    # Drivers Telemetry Data
    driver1Tel = pd.DataFrame()
    driver2Tel = pd.DataFrame()

    # Loops Through Every Lap In The Race To Find The Inputted One
    for index1, row1 in driver1Laps.iterlaps():
        if str(int(row1['LapNumber'])) == lap:
            driver1Tel = row1.get_telemetry().add_distance()

    for index2, row2 in driver2Laps.iterlaps():
        if str(int(row2['LapNumber'])) == lap:
            driver2Tel = row2.get_telemetry().add_distance()

    # Increase The Plot Size
    plt.rcParams['figure.figsize'] = plotSize

    # Creates The Plot
    fig, ax = plt.subplots(6, gridspec_kw={'height_ratios': plotRatios}, sharex=True)

    # Sets The Plots Title
    ax[0].title.set_text("Lap " + lap + " Telemetry For " + driver1 + " & " + driver2 + "\n" + F1Session.weekend.name + " " + str(F1Session.weekend.year))

    # Plots
    ax[0].plot(driver1Tel['Distance'], driver1Tel['Speed'], color=fastf1.plotting.team_color(driver1Info.team), label=driver1)
    ax[0].plot(driver2Tel['Distance'], driver2Tel['Speed'], color=fastf1.plotting.team_color(driver2Info.team), label=driver2)
    ax[0].set(ylabel='Speed')
    ax[0].legend(loc="lower right")

    ax[1].plot(driver1Tel['Distance'], driver1Tel['Throttle'], color=fastf1.plotting.team_color(driver1Info.team), label=driver1)
    ax[1].plot(driver2Tel['Distance'], driver2Tel['Throttle'], color=fastf1.plotting.team_color(driver2Info.team), label=driver2)
    ax[1].set(ylabel='Throttle')

    ax[2].plot(driver1Tel['Distance'], driver1Tel['Brake'], color=fastf1.plotting.team_color(driver1Info.team), label=driver1)
    ax[2].plot(driver2Tel['Distance'], driver2Tel['Brake'], color=fastf1.plotting.team_color(driver2Info.team), label=driver2)
    ax[2].set(ylabel='Brake')

    ax[3].plot(driver1Tel['Distance'], driver1Tel['nGear'], color=fastf1.plotting.team_color(driver1Info.team), label=driver1)
    ax[3].plot(driver2Tel['Distance'], driver2Tel['nGear'], color=fastf1.plotting.team_color(driver1Info.team), label=driver2)
    ax[3].set(ylabel='Gear')

    ax[4].plot(driver1Tel['Distance'], driver1Tel['RPM'], color=fastf1.plotting.team_color(driver1Info.team), label=driver1)
    ax[4].plot(driver2Tel['Distance'], driver2Tel['RPM'], color=fastf1.plotting.team_color(driver2Info.team), label=driver2)
    ax[4].set(ylabel='RPM')

    ax[5].plot(driver1Tel['Distance'], driver1Tel['DRS'], color=fastf1.plotting.team_color(driver1Info.team), label=driver1)
    ax[5].plot(driver2Tel['Distance'], driver2Tel['DRS'], color=fastf1.plotting.team_color(driver2Info.team), label=driver2)
    ax[5].set(ylabel='DRS')
    ax[5].set(xlabel='Distance In Meters')

    # Cleans Up The Tick Labels
    for a in ax:
        a.label_outer()

    # Outputs The Plot
    plt.show()