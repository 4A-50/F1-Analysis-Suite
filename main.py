#<editor-fold desc="Imports">
import argparse
import time
from rich.console import Console
from rich.style import Style

import FTPLT
import FLMS
#</editor-fold>

#<editor-fold desc="Set Ups">
console = Console(highlight = False)
mainStyle = Style(color = "yellow")
errorStyle = Style(color = "red")
#</editor-fold>

#<editor-fold desc="Argument Parser">
parser = argparse.ArgumentParser()
parser.add_argument("mode", help = "The Analysis Mode", type = str)
parser.add_argument("driver", help = "Drivers Three Letter Identifier Or Driver Number")
parser.add_argument("-y", "--year", help = "The Year For Session (E.G. 2021)", type = int)
parser.add_argument("-r", "--race", help = "The Race Number(E.G. 10 (Austria))", type = int)
parser.add_argument("-s", "--session", help = "The Session Name (E.G. R, SQ, Q, FP3, FP2, FP1)")
parser.add_argument("-m", "--minisectors", help = "The Amount Of MiniSectors", type = int)
parser.add_argument("-sp", "--startingpos", help = "The Drivers Starting Position", type = int)
parser.add_argument("-v", "--verbose", help="Increase The Output Verbosity", action="store_true")
#</editor-fold>

args = parser.parse_args()
start_time = time.time()

if args.mode == "FTPLT":
    #Check The Needed Args Are Supplied
    if args.year is not None and args.race is not None and args.session is not None:
        FTPLT.FastestTechnicallyPossibleLapTime(args.driver, args.year, args.race, args.session, args.minisectors, args.verbose)
        console.print("Program Completed In " + str(time.time() - start_time) + " Seconds", style=mainStyle)
    else:
        console.print("Incorrect Arguments Inputted", style=errorStyle)
elif args.mode == "FLMS":
    if args.year is not None and args.race is not None and args.session is not None:
        FLMS.FastestLapMiniSectors(args.driver, args.year, args.race, args.session, args.minisectors)
        console.print("Program Completed In " + str(time.time() - start_time) + " Seconds", style=mainStyle)
    else:
        console.print("Incorrect Arguments Inputted", style=errorStyle)
elif args.mode == "PRP":
    if args.startingpos is not None:
        print("Predicted Race Position")
        console.print("Program Completed In " + str(time.time() - start_time) + " Seconds", style=mainStyle)
    else:
        console.print("Incorrect Arguments Inputted", style=errorStyle)
else:
    console.print("Incorrect Mode Inputted", style=errorStyle)