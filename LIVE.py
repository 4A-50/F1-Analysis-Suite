#<editor-fold desc="Imports">
import fastf1 as ff1
import pandas as pd
import datetime
from rich.console import Console
from rich.table import Table
from rich import box
from rich.style import Style
from requests import Session
from signalr import Connection
#</editor-fold>

#<editor-fold desc="Set Ups">
pd.options.mode.chained_assignment = None

console = Console(highlight = False)
mainStyle = Style(color = "yellow")
#</editor-fold>

def LiveTiming(username, password):
    #LiveTimingResults()
    with Session() as session:
        # create a connection
        connection = Connection("https://livetiming.formula1.com/signalr", session)

        # get chat hub
        chat = connection.register_hub('chat')

        # start a connection
        connection.start()

        # create new chat message handler
        def print_received_message(data):
            print('received: ', data)

        # create new chat topic handler
        def print_topic(topic, user):
            print('topic: ', topic, user)

        # create error handler
        def print_error(error):
            print('error: ', error)

        # receive new chat messages from the hub
        chat.client.on('newMessageReceived', print_received_message)

        # process errors
        connection.error += print_error

        # start connection, optionally can be connection.start()
        with connection:
            # post new message
            #chat.server.invoke('send', 'Python is here')

            # change chat topic
            #chat.server.invoke('setTopic', 'Welcome python!')

            # invoke server method that throws error
            #chat.server.invoke('requestError')

            # post another message
           # chat.server.invoke('send', 'Bye-bye!')

            # wait a second before exit
            connection.wait(1)

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