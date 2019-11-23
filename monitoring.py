"""
__author__  =  ('ABHISEK GANGULY' , 'ASHUTOSH NAYAK')
GITHUB REPO OF THE FULL PROJECT = https://github.com/AbhisekGanguly/Live-Plant-Monitoring-system

ABHISEK GANGULY = 'https://github.com/AbhisekGanguly'
ASHUTOSH NAYAK = 'https://github.com/ashklempton'

LICENSE = MIT (Open Source) License 
python version used = 3.7
"""


import serial  # importing serial library
import numpy  # importing numpy for array maths
import matplotlib.pyplot as plt  # importing matplotlib library
from drawnow import *  # importing drawnow
from pymongo import MongoClient
import time  # importing time

DB_URI = "mongodb://ash_k:singleaf202@ds161346.mlab.com:61346/plant-monitoring?retryWrites=false"

DB_NAME = "plant-monitoring"

client = MongoClient(DB_URI)
db = client[DB_NAME]

humid = []  # taking empty array for plotting graph
tempC = []  # taking empty array for plotting graph
count = 0  # making a counter

# connecting python to the serial port
arduinoData = serial.Serial("COM5", 9600)
plt.ion()  # telling matplotlib that I'll be plotting live data


def makeFig():  # create a function that makes our desired plot
    plt.ylim(15, 35)  # creating a limit on th yaxis expansion
    plt.title("Live plant monitoring system")  # giving title to the project
    plt.grid(True)  # making grid in the graph for better representation
    plt.ylabel("Temperature Celcius")  # adding the temperature label
    # plotting the temperature data
    plt.plot(tempC, "ro-", label="Degree Celcius")
    plt.legend(loc="upper left")  # giving location to the temperature legend

    plt2 = plt.twinx()  # twin of the x axis for humidity
    plt2.plot(humid, "b^-", label="Humidity")  # plotting data for the humidity
    plt.legend(loc="upper right")  # giving location to the humidity legend
    # force matplotlib not to autoscale Y
    plt2.ticklabel_format(useOffset=False)


while True:  # infinity while loop
    while arduinoData.inWaiting() == 0:  # waits here until there's data
        pass  # Does nothing, only passes the data
    arduinoString = arduinoData.readline()  # reads the data from the serial port
    arduinoString = arduinoString.decode()  # decode the read data

    dataArray = arduinoString.split(",")  # spliting the data into two array
    humidity = float(dataArray[0])  # taking humidity value as float
    temperature = float(dataArray[1])  # taking temperature value as float

    # try adding data to database
    timestamp = time.time()
    obj = {"temperature": temperature, "humidity": humidity, "timestamp": timestamp}

    try:
        db.data.insert_one(obj)
        print("data added")
    except:
        print("some error occured")
        print(e)

    tempC.append(temperature)  # appending values to temperature array
    humid.append(humidity)  # appending values to humidity array
    drawnow(makeFig)  # drawing the function using drawnow
    plt.pause(0.00001)  # pausing the plot for few nano seconds

    count += 1  # making a counter
    if count > 50:  # making an if statement for popping the old data
        tempC.pop(0)  # popping the old temperature data
        humid.pop(0)  # popping the old humidity data
