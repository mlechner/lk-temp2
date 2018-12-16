#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import time
from Config import Config
from time import sleep
import RPi.GPIO as GPIO


class LKTemp2App:
    def __init__(self, *args, **kwargs):
        self.config = Config().get_config()
        self.timeconf = self.config['time']
        self.deviceconf = self.config['device']
        self.sleeptime = float(self.timeconf['sleeptime'])
        self.base_dir = self.deviceconf['base_dir']
        # Der One-Wire EingangsPin wird deklariert und der integrierte PullUp-Widerstand aktiviert
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Nach Aktivierung des Pull-UP Widerstandes wird gewartet,
        # bis die Kommunikation mit dem DS18B20 Sensor aufgebaut ist
        print 'Warte auf Initialisierung...'
        while True:
            try:
                self.device_folder = glob.glob(self.base_dir + self.deviceconf['device_folder'])[0]
                break
            except IndexError:
                sleep(0.5)
                continue
        self.device_file = self.device_folder + self.deviceconf['device_file']
        self.lines = None
        self.temp_c = None
        # Zur Initialisierung, wird der Sensor einmal "blind" ausgelesen
        self.temperature_reading()

    # Funktion wird definiert, mit dem der aktuelle Messwert am Sensor ausgelesen werden kann
    def temperature_reading(self):
        f = open(self.device_file, 'r')
        self.lines = f.readlines()
        f.close()

    # Die Temperaturauswertung: Beim Raspberry Pi werden erkannte one-Wire Slaves im Ordner
    # /sys/bus/w1/devices/ einem eigenen Unterordner zugeordnet. In diesem Ordner befindet sich die Datei w1-slave
    # in dem Die Daten, die über dem One-Wire Bus gesendet wurden gespeichert.
    # In dieser Funktion werden diese Daten analysiert und die Temperatur herausgelesen und ausgegeben
    def temperature_analysis(self):
        self.temperature_reading()
        while self.lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            self.temperature_reading()
        equals_pos = self.lines[1].find('t=')
        if equals_pos != -1:
            temp_string = self.lines[1][equals_pos+2:]
            self.temp_c = float(temp_string) / 1000.0

    # Hauptprogrammschleife
    # Die gemessene Temperatur wird in die Konsole ausgegeben - zwischen den einzelnen Messungen
    # ist eine Pause, deren Länge mit der Variable "sleeptime" eingestellt werden kann
    def run(self):
        try:
            while True:
                self.temperature_analysis()
                print "Temperatur:", self.temp_c, "°C"
                time.sleep(self.sleeptime)
        except KeyboardInterrupt:
            self.GPIO.cleanup()


if __name__ == "__main__":
    app = LKTemp2App()
    app.run()
