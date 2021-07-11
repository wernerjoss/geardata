#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Programm zur Berechnung / Darstellung von Gangdiagrammen für Motorräder, analog des bekannten geardata.
# Anders als dort können hier jedoch zwei komplette Diagramme übereinander gelegt und somit einfacher verglichen werden.
# Ebenso wird der Drehzahlabfall beim Hochschalten angezeigt.
# Die Eingabedaten (Parameter) sind in yaml Files gespeichert, 2 Beispiele sind hier angefügt, eigentlich selbsterklärend.
# Momentan ist es ein einfaches Kommandozeilen-Programm mit 1 oder 2 Parameter-Files als Argument(e)
# Die einzige Nonstandard-Python Library die benötigt wird ist aktuell matplotlib
# ggf. folgt hier auch noch eine GUI Version auf Basis von PyQt5... (wobei jeder der einen Editor bedienen kann, hier sehr schnell verschiedene Setups vergleichen kann)

import sys, yaml
import matplotlib.pyplot as plt

Verbose = True
StartRPM = 0    #   8500

def get_params(datafile):
    with open(datafile) as f:
        try:
            ymldata = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            quit()
    global IP
    IP = float(ymldata['IP'][0].split(':')[0]) / float(ymldata['IP'][0].split(':')[1])
    global Ig
    Ig = []
    for IG in ymldata['IGtr']:
        Ig.append(float(IG.split(':')[0]) / float(IG.split(':')[1]))
    global ISek
    ISek = float(ymldata['ISek'][0].split(':')[0]) / float(ymldata['ISek'][0].split(':')[1])
    global TyreCirc
    TyreCirc = float(ymldata['TyreCirc'])
    global RefRPM
    RefRPM = int(ymldata['RefRPM'])
    if (Verbose):
        print("IP:%f" % IP)
        print("Igtr:")
        print(Ig)
        print("ISek:%f" % ISek)
        print("TyreCirc: %f" % TyreCirc)
        print("RPM: %d" % RefRPM)

datafile0 = ''
datafile1 = ''
if (len(sys.argv) <= 1):
    print('Usage: %s datafile1 <datafile2>' % sys.argv[0])
    quit()
if (len(sys.argv) > 1):
    datafile0 = sys.argv[1]
if (len(sys.argv) > 2):
    datafile1 = sys.argv[2]

get_params(datafile0)
nextG = 1
NumGears = len(Ig) - 1
for Igang in Ig:
    x = [StartRPM, RefRPM, RefRPM*(Ig[nextG]/Igang)]
    EndSpeed = (RefRPM/IP/Igang/ISek*TyreCirc)*60/1000
    y = [(StartRPM/IP/Igang/ISek*TyreCirc)*60/1000, EndSpeed, EndSpeed]
    plt.plot(x,y, color='red')
    if (nextG < NumGears):
        nextG = nextG + 1

if (len(datafile1) > 0):
    get_params(datafile1)
    nextG = 1
    NumGears = len(Ig) - 1
    for Igang in Ig:
        x = [StartRPM, RefRPM, RefRPM*(Ig[nextG]/Igang)]
        EndSpeed = (RefRPM/IP/Igang/ISek*TyreCirc)*60/1000
        y = [(StartRPM/IP/Igang/ISek*TyreCirc)*60/1000, EndSpeed, EndSpeed]
        plt.plot(x,y, color='blue')
        if (nextG < NumGears):
            nextG = nextG + 1

Title = datafile0;
if (len(datafile1) > 0):
    Title = Title + ' / ' + datafile1
plt.title(Title)
plt.ylabel('Km/H')
plt.xlabel('RPM')
plt.grid(True)
plt.show()
