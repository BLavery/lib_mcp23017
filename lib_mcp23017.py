#!/usr/bin/python
# -*- coding: utf-8 -*-

# A totally simple bit-based I/O class for 16 digital pins on MCP23107. No interrupts, no inversions.
# Syntax mirrors regular digital self.GPIO I/O
# Supports multiple MCP devices by one MCP23017 object for each

# Tie MCP23017's RST: (1) to arduino RST. That resets mcp with each arduino hard or DTR reset.
# (2) or simply tied HIGH (not preferred)
# (3) or driven from a regular self.GPIO pin to control reset (RPI preference)


# mcp23017.pdf refs are on internet.
# SMBus syntax
# MCP is divided into 2 8-bit ports but this library refers to pins as simply 0-15

import sys

if __name__ == '__main__':
    print (sys.argv[0], 'is an importable module:')
    print ("...  from", sys.argv[0], "import MCP23017")
    exit()


def _BV(x):
    return (1<<x)

import time
import sys


# Registers of MCP23017:
IODIRA = 0x00   # pin direction
IODIRB = 0x01
OLATA = 0x14    # outputs
OLATB = 0x15
GPIOA = 0x12    # inputs
GPIOB = 0x13
GPPUA = 0x0c    # pullups
GPPUB = 0x0d


class MCP23017:
    GPIO = None
    bus = None

    def __init__(self, gpio, bus, addr, rstPin = (-1)):
        # rstPin is optional: a self.GPIO pin for resetting the MCP device
        self.GPIO = gpio
        self.bus = bus
        self.addr = addr
        if rstPin > 0:
            # Use our nominated reset pin to init the mcp23017
            self.GPIO.setup(rstPin, self.GPIO.OUT)
            self.GPIO.output(rstPin, self.GPIO.LOW)
            time.sleep(0.01)
            self.GPIO.output(rstPin, self.GPIO.HIGH)
            time.sleep(0.01)
        f = self.bus.read_byte_data(self.addr, IODIRA)*256 + (self.bus.read_byte_data(self.addr, OLATA))
        if not (f == 0xff00):   # not in reset state. Try some software remedy. At least make all inputs:
            self.bus.write_byte_data(addr, IODIRA, 0xff)
            self.bus.write_byte_data(addr, IODIRB, 0xff)
        f = self.bus.read_byte_data(self.addr, IODIRA)*256 + (self.bus.read_byte_data(self.addr, OLATA))
        self.found = (f == 0xFF00)  # a "lightweight" test!
        # So caller can test that MCP device was found correctly and was reset OK.

    def setup(self, dpin, mode, pull_up_down=0):
        if dpin>15:
            return
        if pull_up_down == self.GPIO.PUD_DOWN:
            print ("Warning: MCP23017 has no pulldown. Continuing ...")
        pup = (pull_up_down == self.GPIO.PUD_UP)
        dirOUT = (mode == self.GPIO.OUT)
        portb = dpin >> 3   #  = 0 for portA (0-7) and 1 for portB (8-15)
        dpin &= 7           # = always 0-7
        pdata = self.bus.read_byte_data(self.addr, portb+GPPUA)
        if pup:
            pdata |= _BV(dpin)
        else:
            pdata &= (~(_BV(dpin)))
        self.bus.write_byte_data(self.addr, portb+GPPUA, pdata)  # pullups

        ddata = self.bus.read_byte_data(self.addr, portb+IODIRA)
        if dirOUT:
            ddata &= (~(_BV(dpin)))
        else:
            ddata |= _BV(dpin)
        self.bus.write_byte_data(self.addr, portb+IODIRA, ddata)   # pin direction


    def output(self, dpin, hilo):
        if dpin > 15:
            return
        portb = dpin >> 3
        dpin &= 7
        data = self.bus.read_byte_data(self.addr, portb+GPIOA)
        if hilo:
            data |= _BV(dpin)
        else:
            data &= (~(_BV(dpin)))
        self.bus.write_byte_data(self.addr, portb+OLATA, data)



    def input(self, dpin):
        if dpin > 15:
            return 0
        portb = dpin >> 3
        dpin &= 7
        return (self.bus.read_byte_data(self.addr, portb+GPIOA) & _BV(dpin))> 0

    def inputAll(self):
        return [self.bus.read_byte_data(self.addr, GPIOA), self.bus.read_byte_data(self.addr, GPIOB)]

    def outputByte(self, port, data8):
        # port 0 for portA,   1 for portB
        self.bus.write_byte_data(self.addr, (port&1)+OLATA, (data8&0xff))





########################################################################
