# SoundCheck TCP Control Example v1.0
# SoundCheck 17.0 (or greater) must be open and running before executing this script.
# SoundCheck must have TCP/IP server enabled on port 4444
# Sends simple commands to SoundCheck via TCP, and receives responses as JSON strings
#
# Python 3.x compatible
# Requires json
#

import socket
import json
import inspect
import fnmatch
import os
import time
import platform
import subprocess
import sys


# Declare SoundCheckTcp class
class SoundCheckTcp:
    def __init__(self, port):
        self.ip = port[0]
        self.port = port[1]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.connect((self.ip, self.port))
        self.sock.recv(500)  # This should be the Welcome message

    def __del__(self):
        self.sock.close()

    # define command send/receive method for simplified call

    def send(self, cmd):
        cmd_ba = bytearray("%s\r\n" % cmd, "utf8")
        self.sock.send(cmd_ba)
        data = self.sock.recv(100000)
        js = json.loads(data.decode("utf8"))
        if js["cmdCompleted"]:
            return js
        else:
            raise Exception("SoundCheck command did not complete:  %s: %s: %s: %s" %
                            (js["errorDescription"], js["errorType"], js["originalCommand"], data))

    def open(self, filename):
        js = self.send("Sequence.Open('%s')" % filename)
        return js["returnData"]["Value"]

    def setLotNumber(self, lotNumber):
        self.send("SoundCheck.SetLotNumber('%s')" % lotNumber)

    def getLotNumber(self):
        js = self.send("SoundCheck.GetLotNumber")
        return js["returnData"]["Value"]

    def setSerialNumber(self, serialNumber):
        self.send("SoundCheck.SetSerialNumber('%s')" % serialNumber)

    def getSerialNumber(self):
        js = self.send("SoundCheck.GetSerialNumber")
        return js["returnData"]["Value"]

    def setLoginLevel(self, level="engr"):
        self.send("SoundCheck.SetLoginLevel('%s')" % level)

    def getLoginLevel(self):
        js = self.send("SoundCheck.GetLoginLevel")
        return js["returnData"]["Value"]

    def memGetAllNames(self):
        js = self.send("MemoryList.GetAllNames")
        return js["returnData"]

    def run(self):
        js = self.send("Sequence.Run")
        return js["returnData"]["Pass?"]

    def getCurveNames(self):
        return self.memGetAllNames()["Curves"]

    def getWaveformNames(self):
        return self.memGetAllNames()["Waveforms"]

    def getValueNames(self):
        return self.memGetAllNames()["Values"]

    def getResultNames(self):
        return self.memGetAllNames()["Results"]

    def get(self, gtype, name):
        js = self.send("MemoryList.Get('%s', '%s')" % (gtype, name))
        return js["returnData"]

    def getCurve(self, name):
        return self.get('Curve', name)

    def getWaveform(self, name):
        return self.get('Waveform', name)

    def getValue(self, name):
        return self.get('Value', name)

    def getResult(self, name):
        return self.get('Result', name)


def check_tcp_port(port):
    # This function polls a TCP port to see if it is open.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(port)
    return result == 0


def main():

    # Define the TCP port used to communicate with SoundCheck
    sc_port = ('127.0.0.1', 4444)

    # Poll the TCP port periodically until it is opened.
    #print("Checking TCP Port...")
    port_timeout = 60
    while not check_tcp_port(sc_port) and not (port_timeout < 1):
        time.sleep(0.1)#was 0.3
        port_timeout -= 1
    if check_tcp_port(sc_port):
        #print('Port {} is open.'.format(sc_port))
        time.sleep(0.1)#was 10
    else:
        print('Timeout while waiting for port {} to open.'.format(sc_port))
        exit(1)

    try:
        # Communicate with SoundCheck
        sc = SoundCheckTcp(sc_port)

        #print("\n\nSetting serial number")
        sc.setSerialNumber(str(sys.argv[1]))
        #print("\n\nSerial number is %s" % sc.getSerialNumber())

    except socket.timeout:
        print("Socket timed out...exiting...")
        exit(1)

   

    exit(0)


if __name__ == "__main__":
    main()
