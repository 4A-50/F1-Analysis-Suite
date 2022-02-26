#<editor-fold desc="Imports">
import fastf1 as ff1
import pandas as pd
import datetime
from rich.console import Console
from rich.table import Table
from rich import box
from rich.style import Style
#</editor-fold>

#<editor-fold desc="Set Ups">
pd.options.mode.chained_assignment = None

console = Console(highlight = False)
mainStyle = Style(color = "yellow")
#</editor-fold>

def LiveTiming(username, password):
    LiveTimingResults()

def LiveTimingResults():
    # Creates A Table To Output The Results
    outputTable = Table(title="Live Timing\nLap Number:", box=box.SIMPLE, title_style=mainStyle)
    # Adds The Columns
    outputTable.add_column("Driver", justify="center")
    outputTable.add_column("Lap Time", justify="center")
    outputTable.add_column("Sector 1", justify="center", header_style=Style(color= "red"))
    outputTable.add_column("Sector 2", justify="center", header_style=Style(color= "blue"))
    outputTable.add_column("Sector 3", justify="center", header_style=Style(color= "yellow"))

    console.print(outputTable)