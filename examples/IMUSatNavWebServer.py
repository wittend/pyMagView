#!/usr/bin/env python3
#
# IMUSatNavWebServer.py
#
# For serving GPS and IMU Data from an Odroid-C0 or C1
#
# Should work with few changes for many Raspberry-Pi type devices
# running Ubuntu, Debian, or their ilk.
#
# see question:
#   http://stackoverflow.com/questions/37172006/python-3-threaded-websockets-server
#
# Otherwise:
#   Copyright (c) April 4, 2017 by David M. Witten II
#
# changes:
#   June 11, 2017   by DMWII
#   June 13, 2017   by DMWII
#=========================================================================
import signal
import sys
sys.path.append('.')
import os
import os.path
import subprocess
from subprocess import Popen, PIPE
import asyncio
import threading
import http.server
import urllib
from urllib.parse import urlparse
import socket
import socketserver
import select
import time
from time import sleep
from datetime import datetime
import math
from math import modf
import getopt
import argparse
import json
import RTIMU
#import GPS3
from gps3 import gps3

WEB_PORT        = 8000                  # HTTP Port to use
GPSD_HOST       = '127.0.0.1'           # gpsd
GPSD_PORT       = 2947                  # defaults
PROTOCOL        = 'json'                # Use JSON data
GPS_DEVICE      = '/dev/ttyS0'          # Use GPS Device (if not default)

last_worktime   = 0
last_idletime   = 0
stopFlag        = False

__author__      = 'Dave Witten II'
__copyright__   = 'Copyright 2017  Dave Witten II'
__license__     = 'GPL-2'
__version__     = '0.33.2'

CONVERSION = {'raw': (1, 1, 'm/s', 'meters'),
              'metric': (3.6, 1, 'kph', 'meters'),
              'nautical': (1.9438445, 1, 'kts', 'meters'),
              'imperial': (2.2369363, 3.2808399, 'mph', 'feet')}

#---------------------------------------
# add_args()
#---------------------------------------
def add_args():
    """Adds commandline arguments and formatted Help"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-host', action='store', dest='host', default='127.0.0.1', help='DEFAULT "127.0.0.1"')
    parser.add_argument('-port', action='store', dest='port', default='2947', help='DEFAULT 2947', type=int)
    parser.add_argument('-json', dest='gpsd_protocol', const='json', action='store_const', default='json', help='DEFAULT JSON objects */')
    parser.add_argument('-device', dest='devicepath', action='store', help='alternate devicepath e.g.,"-device /dev/ttyS2"')
    # Infrequently used options
    parser.add_argument('-nmea', dest='gpsd_protocol', const='nmea', action='store_const', help='*/ output in NMEA */')
    parser.add_argument('-v', '--version', action='version', version='Version: {}'.format(__version__))
    cli_args = parser.parse_args()
    return cli_args

#---------------------------------------
# satellites_used()
#---------------------------------------
def satellites_used(feed):
    """Counts number of satellites used in calculation from total visible satellites
    Arguments:
        feed feed=data_stream.TPV['satellites']
    Returns:
        total_satellites(int):
        used_satellites (int):
    """
    total_satellites = 0
    used_satellites  = 0

    if not isinstance(feed, list):
        return 0, 0

    for satellites in feed:
        total_satellites += 1
        if satellites['used'] is True:
            used_satellites += 1
    return total_satellites, used_satellites


#---------------------------------------
# make_time()
#---------------------------------------
def make_time(gps_datetime_str):
    """Makes datetime object from string object"""
    if not 'n/a' == gps_datetime_str:
        datetime_string = gps_datetime_str
        datetime_object = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S")
        return datetime_object


#---------------------------------------
# elapsed_time_from()
#---------------------------------------
def elapsed_time_from(start_time):
    """calculate time delta from latched time and current time"""
    time_then = make_time(start_time)
    time_now = datetime.utcnow().replace(microsecond=0)
    if time_then is None:
        return
    delta_t = time_now - time_then
    return delta_t


#---------------------------------------
# unit_conversion()
#---------------------------------------
def unit_conversion(thing, units, length=False):
    """converts base data between metric, imperial, or nautical units"""
    if 'n/a' == thing:
        return 'n/a'
    try:
        thing = round(thing * CONVERSION[units][0 + length], 2)
    except TypeError:
        thing = 'fubar'
    return thing, CONVERSION[units][2 + length]

#---------------------------------------
# get_cpu_usage()
#---------------------------------------
def get_cpu_usage():
    global last_worktime, last_idletime
    try:
        f = open("/proc/stat","r")
    except:
        return 0                        # Workaround, possibly we're on a Mac
    line = ""
    while not "cpu " in line:
        line=f.readline()
    f.close()
    spl=line.split(" ")
    worktime  = int(spl[2])+int(spl[3])+int(spl[4])
    idletime  = int(spl[5])
    dworktime = (worktime-last_worktime)
    didletime = (idletime-last_idletime)
    rate = float(dworktime)/(didletime+dworktime)
    last_worktime = worktime
    last_idletime = idletime
    if(last_worktime == 0):
        return 0
    return rate

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# class GPSWorker
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class GPSWorker (threading.Thread):
    #---------------------------------------
    # __init__()
    #---------------------------------------
    def __init__(self):
        threading.Thread.__init__(self)
        self.data = 0
        self.lastData = 0
        self.inc = 0
        print("Using GPSD Host: " + GPSD_HOST + " Port: " + str(GPSD_PORT))
        self.gpsd = gps3.GPSDSocket()
        self.gpsd.connect(GPSD_HOST, GPSD_PORT)
        self.gpsd.watch(gpsd_protocol = PROTOCOL)     # args.gpsd_protocol)
#        self.fix = gps3.Fix()
        self.data_stream = gps3.DataStream()

    #---------------------------------------
    # run()
    #---------------------------------------
    def run(self):
        form = 'RAW'
        units = 'raw'
        while not stopFlag:
            for new_data in self.gpsd:               # gpsd:
                if new_data:
                    self.data_stream.unpack(new_data)
                    self.curtime  = ('{time}'.format(**self.data_stream.TPV))
                    self.curalt   = ('{}'.format(self.data_stream.TPV['alt']))
                    self.curlat   = ('{}'.format(self.data_stream.TPV['lat']))
                    self.curlon   = ('{}'.format(self.data_stream.TPV['lon']))
                    self.curspeed = ('{} {}'.format(*unit_conversion(self.data_stream.TPV['speed'], units)))
                    self.curhead  = ('{track}'.format(**self.data_stream.TPV))
                    self.curclimb = ('{} {}/s'.format(*unit_conversion(self.data_stream.TPV['climb'], units, length=True)))
                    self.curstat  = ('{mode:<}D  '.format(**self.data_stream.TPV))

                    if isinstance(self.data_stream.SKY['satellites'], list):  # Nested lists of dictionaries are strings before data is present
                        self.satinfo = ''
                        b = 0
                        for sats in self.data_stream.SKY['satellites'][0:10]:
#                            self.satinfo = self.satinfo + ('{{"prn": "{PRN:>2}", "el": "{el:>6}", "az": "{az:>5}", "ss": "{ss:>5}",  "inuse":"{used:}"}}').format(**sats)
                            if(b > 0):
                                self.satinfo = self.satinfo + ','
                            self.satinfo = self.satinfo + ('{{"prn": {PRN:>2}, "el": {el:>6}, "az": {az:>5}, "ss": {ss:>5},  "inuse": "{used:}"}}').format(**sats)
                            b = b + 1

                self.data = self.data_stream.TPV
            time.sleep(1)

    #---------------------------------------
    # get()
    #---------------------------------------
    def get(self):
        if self.lastData is not self.data:
            self.lastData = self.data
            return self.data

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# class IMUWorker
# //////// getIMUData
# {"getIMUData", (PyCFunction)([] (PyObject *self, PyObject* args) -> PyObject* {
#     const RTIMU_DATA& data = ((RTIMU_RTIMU*)self)->val->getIMUData();
#     return Py_BuildValue("{s:K,s:O,s:(d,d,d),s:O,s:(d,d,d,d),s:O,s:(d,d,d),s:O,s:(d,d,d),s:O,s:(d,d,d),s:O,s:d,s:O,s:d,s:O,s:d}",
#              "timestamp", data.timestamp,
#              "fusionPoseValid", PyBool_FromLong(data.fusionPoseValid),
#              "fusionPose", data.fusionPose.x(), data.fusionPose.y(), data.fusionPose.z(),
#              "fusionQPoseValid", PyBool_FromLong(data.fusionQPoseValid),
#              "fusionQPose", data.fusionQPose.scalar(), data.fusionQPose.x(), data.fusionQPose.y(), data.fusionQPose.z(),
#              "gyroValid", PyBool_FromLong(data.gyroValid),
#              "gyro", data.gyro.x(), data.gyro.y(), data.gyro.z(),
#              "accelValid", PyBool_FromLong(data.accelValid),
#              "accel", data.accel.x(), data.accel.y(), data.accel.z(),
#              "compassValid", PyBool_FromLong(data.compassValid),
#              "compass", data.compass.x(), data.compass.y(), data.compass.z(),
#              "pressureValid", PyBool_FromLong(data.pressureValid),
#              "pressure", data.pressure,
#              "temperatureValid", PyBool_FromLong(data.temperatureValid),
#              "temperature", data.temperature,
#              "humidityValid", PyBool_FromLong(data.humidityValid),
#              "humidity", data.humidity);
#     }),
# METH_NOARGS,
# "Return true if valid bias" },
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class IMUWorker (threading.Thread):
    #---------------------------------------
    # __init__()
    #---------------------------------------
    def __init__(self):
        threading.Thread.__init__(self)
        self.data = 0
        self.lastData = 0
        # set some gyro rate here to test (units: rads/s)
        self.gx = 0.0
        self.gy = 0.0
        self.gz = 0.1
        # set accel to indicate horizontal (units: g)
        self.ax = 0.0
        self.ay = 0.0
        self.az = 1.0
        # set mag to whatever (or leave as 0 if turned off) (units: uT)
        self.mx = 0.0
        self.my = 0.0
        self.mz = 0.0
        SETTINGS_FILE = "RTIMULib"
        print("Using IMU settings file " + SETTINGS_FILE + ".ini")
        if not os.path.exists(SETTINGS_FILE + ".ini"):
            print("IMU Settings file does not exist, will be created")
        self.s = RTIMU.Settings(SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(self.s)
        print("IMU Name: " + self.imu.IMUName())
        self.poll_interval = self.imu.IMUGetPollInterval()
        print("Recommended Poll Interval: %dmS\n" % self.poll_interval)

        # Dont forget this!
        self.imu.IMUInit()
        # this is how to turn off/on the the IMU components
        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

    #---------------------------------------
    # run()
    #---------------------------------------
    def run(self):
        while not stopFlag:
            if self.imu.IMURead():
                self.data       = self.imu.getIMUData()
                # self.timestamp  = self.data["timestamp"]
                self.fusionPose = self.data["fusionPose"]
                self.roll       = ('%f' % (math.degrees(self.fusionPose[0])))
                self.pitch      = ('%f' % (math.degrees(self.fusionPose[1])))
                self.yaw        = ('%f' % (math.degrees(self.fusionPose[2])))

                self.compass    = self.data["compass"]
                self.mx         = ('%f' % self.compass[0])      # (math.degrees(self.compass[0])))
                self.my         = ('%f' % self.compass[1])      # (math.degrees(self.compass[1])))
                self.mz         = ('%f' % self.compass[2])      # (math.degrees(self.compass[2])))

                self.accel      = self.data["accel"]
                self.ax         = ('%f' % self.accel[0])        # (math.degrees(self.compass[0])))
                self.ay         = ('%f' % self.accel[1])        # (math.degrees(self.compass[1])))
                self.az         = ('%f' % self.accel[2])        # (math.degrees(self.compass[2])))

                self.gyro       = self.data["gyro"]
                self.gx         = ('%f' % self.gyro[0])         # (math.degrees(self.compass[0])))
                self.gy         = ('%f' % self.gyro[1])         # (math.degrees(self.compass[1])))
                self.gz         = ('%f' % self.gyro[2])         # (math.degrees(self.compass[2])))

            time.sleep(0.08)

    #---------------------------------------
    # get()
    #---------------------------------------
    def get(self):
        if self.lastData is not self.data:
            self.lastData = self.data
            return self.data

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# class RequestHandler()
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class RequestHandler(http.server.SimpleHTTPRequestHandler):                         # BaseHTTPRequestHandler):

    #---------------------------------------
    # _set_headers()
    #---------------------------------------
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    #---------------------------------------
    # do_HEAD()
    #---------------------------------------
    def do_HEAD(self):
        self._set_headers()

    #---------------------------------------
    # do_POST()
    #---------------------------------------
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

    #---------------------------------------
    # do_GET()
    #---------------------------------------
    def do_GET(self):
        form  = 'RAW'
        units = 'raw'
        p = self.path
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # GPS sats-in-view
        #----------------------------------
        if((p == '/sats') or (p == '/sats/')):
            self.wfile.write(bytes('{"sats" : [',       'utf-8'))
            self.wfile.write(bytes(gpsWorker.satinfo,   'utf-8'))
            self.wfile.write(bytes("] }",               'utf-8'))

        # IMU data Request
        #----------------------------------
        elif((p == '/imu') or (p == '/imu/')):
            self.gpsCurTime  = gpsWorker.curtime
            self.gpsLat      = gpsWorker.curlat
            self.gpsLon      = gpsWorker.curlon
            #self.gpsHead     = gpsWorker.curhead
            self.imuRoll     = imuWorker.roll
            self.imuPitch    = imuWorker.pitch
            self.imuYaw      = imuWorker.yaw
            self.imuMx       = imuWorker.mx
            self.imuMy       = imuWorker.my
            self.imuMz       = imuWorker.mz

            self.imuAx       = imuWorker.ax
            self.imuAy       = imuWorker.ay
            self.imuAz       = imuWorker.az

            self.imuGx       = imuWorker.gx
            self.imuGy       = imuWorker.gy
            self.imuGz       = imuWorker.gz

            self.wfile.write(bytes('{ ', 'utf-8'))

            self.wfile.write(bytes('"time": "'   + (self.gpsCurTime)    + '",', 'utf-8'))
            self.wfile.write(bytes('"lat": "'    + (self.gpsLat)        + '",', 'utf-8'))
            self.wfile.write(bytes('"lon": "'    + (self.gpsLon)        + '",', 'utf-8'))
            #self.wfile.write(bytes('"head": "'   + (self.gpsHead)       + '",', 'utf-8'))

            self.wfile.write(bytes('"roll": "'   + (self.imuRoll)       + '",', 'utf-8'))
            self.wfile.write(bytes('"pitch": "'  + (self.imuPitch)      + '",', 'utf-8'))
            self.wfile.write(bytes('"yaw": "'    + (self.imuYaw)        + '",', 'utf-8'))

            self.wfile.write(bytes('"mx": "'     + (self.imuMx)         + '",', 'utf-8'))
            self.wfile.write(bytes('"my": "'     + (self.imuMy)         + '",', 'utf-8'))
            self.wfile.write(bytes('"mz": "'     + (self.imuMz)         + '",', 'utf-8'))

            self.wfile.write(bytes('"ax": "'     + (self.imuAx)         + '",', 'utf-8'))
            self.wfile.write(bytes('"ay": "'     + (self.imuAy)         + '",', 'utf-8'))
            self.wfile.write(bytes('"az": "'     + (self.imuAz)         + '",', 'utf-8'))

            self.wfile.write(bytes('"gx": "'     + (self.imuGx)         + '",', 'utf-8'))
            self.wfile.write(bytes('"gy": "'     + (self.imuGy)         + '",', 'utf-8'))
            self.wfile.write(bytes('"gz": "'     + (self.imuGz)         + '"',  'utf-8'))

            self.wfile.write(bytes(" }", 'utf-8'))

        # GPS data Request
        #----------------------------------
        elif((p == '/gps') or (p == '/gps/')):
            self.gpsCurTime  = gpsWorker.curtime
            self.gpsCurLat   = gpsWorker.curlat
            self.gpsCurLon   = gpsWorker.curlon
            self.gpsCurHead  = gpsWorker.curhead
            self.gpsCurSpeed = gpsWorker.curspeed
            self.gpsCurClimb = gpsWorker.curclimb
            self.gpsCurStat  = gpsWorker.curstat

            self.wfile.write(bytes("{ ", 'utf-8'))

            self.wfile.write(bytes('"time" :  "' + (self.gpsCurTime)  + '",', 'utf-8'))
            self.wfile.write(bytes('"lat"  :  '  + (self.gpsCurLat)   + ',',  'utf-8'))
            self.wfile.write(bytes('"lon"  :  '  + (self.gpsCurLon)   + ',',  'utf-8'))
            self.wfile.write(bytes('"head" :  '  + (self.gpsCurHead)  + ',',  'utf-8'))
            self.wfile.write(bytes('"speed":  "' + (self.gpsCurSpeed) + '",', 'utf-8'))
            self.wfile.write(bytes('"climb":  "' + (self.gpsCurClimb) + '",', 'utf-8'))
            self.wfile.write(bytes('"stat" :  "' + (self.gpsCurStat)  + '"',  'utf-8'))

            self.wfile.write(bytes(" }", 'utf-8'))

        # General info
        #----------------------------------
        elif((p == '/info') or (p == '/info/')):
            self.wfile.write(bytes("{ ", 'utf-8'))
            #---------------------------------------
            # Get the CPU Temperature
            #---------------------------------------
            process = Popen(["cat", "/sys/devices/virtual/thermal/thermal_zone0/temp"], stdout=PIPE)
            (output, err) = process.communicate()
            exit_code = process.wait()
            self.wfile.write(bytes(' "temp": {0:.2f}, '.format(float(output)/1000), 'utf-8'))

            #---------------------------------------
            # Get the Battery Voltage
            #---------------------------------------
            a2dRes = 0.004106
            a2dPath = "/sys/class/saradc/saradc_ch0"
            process = Popen(["cat", a2dPath], stdout=PIPE)
            (a2dValue, err) = process.communicate()
            exit_code = process.wait()
            self.wfile.write(bytes('"voltage": {0:.2f}, '.format(float(a2dValue)*a2dRes), 'utf-8'))

            #---------------------------------------
            # Get the CPU Usage
            #---------------------------------------
            cpu = get_cpu_usage()
            self.wfile.write(bytes('"cpu": {0:.2f} '.format(float(cpu)*100), 'utf-8'))
            self.wfile.write(bytes(" }", 'utf-8'))

        # Otherwise respond to unknown request
        #----------------------------------
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("Whadda ya Want??", 'utf-8'))
            self.wfile.write(bytes("        <br>" + self.path + "", 'utf-8'))


#---------------------------------------
# main()
#---------------------------------------
if __name__ == "__main__":
    args = add_args()
    print('CERC-Nav server')

    gpsWorker = GPSWorker()
    imuWorker = IMUWorker()
#    msgWorker = MSGWorker()

    try:
        gpsWorker.start()
        imuWorker.start()

        handler = RequestHandler                                              # http.server.SimpleHTTPRequestHandler

        httpd = socketserver.TCPServer(("", WEB_PORT), handler)
        print("Serving HTTP at port", WEB_PORT)
        httpd.serve_forever()

    except KeyboardInterrupt:
        stopFlag = True
#        httpd.shutdown()
        print('Keyboard interrupt received\nTerminated by user\nGood Bye.\n')
        sys.exit(0)

    except (OSError, IOError) as error:
        stopFlag = True
#        httpd.shutdown()
        sys.stderr.write('\rServer error--> {}'.format(error))
        sys.stderr.write('\rConnection to gpsd at \'{0}\' on port \'{1}\' failed.\n'.format(args.host, args.port))
        sys.exit(1)
