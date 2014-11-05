
# Setup:
# 5V or 3.3V operation.
# Tie mcp RST to arduino RST (but see resetPin notes below)
# a0 a1 a2 to high (address 0x27) - or as you choose
# mcp to arduino    SDA - SDA  and  SCL - SCL      (or equiv on RPI)
# RPI has i2c pullups already.
# Arduino uses its large internal pullups, marginal. Recomment extra external pullups (eg 4k7).

# These MCP pins MUST be connected somewhere: A0 A1 A2 RST SDA SCL VDD/VCC VSS/GND

# Add a test LED on mcp pin portb-5  (ie mcp pin 13 if counting 0 - 15)

from smartGPIO import GPIO
from lib_mcp23017 import MCP23017
import time

print("")

# We need firstly to create an I2C "bus" object, in the SMBus model:
if GPIO.RPI_REVISION > 0:
        from smbus import SMBus
        i2cbus = SMBus(GPIO.RPI_REVISION-1)  # SMBus(0) or SMBus(1) depending board revision
        resetPin=0
else:
        i2cbus = GPIO.I2C()
        #i2cbus.detect()     # optional diagnostic: find devices on I2C bus.  Comment out when finished with this!
        resetPin = 0

# If parameter resetPin > 0, mcp is hard reset by pulse at initialisation time. (mcp has no proper software reset)
# On arduino, tie mcp RST to arduino RST (DTR triggered), and declare resetPin=0 here (or omit that parameter below)
# On RPI, connect and nominate a (regular GPIO) pin eg BCM pin 18
# Least preferable is to tie mcp reset line HIGH and declare no reset pin here. (Some software reset is then attempted.)

# Now create the MCP expander object, giving it the bus and A0-A2 address (0x20-0x27):
GPIO2 = MCP23017(GPIO, i2cbus, 0x27, resetPin)

#GPIO3 = MCP23017(GPIO, i2cbus, 0x26, resetPin)    # Optional MULTIPLE mcp devices on the i2c bus!
#GPIO4 = MCP23017(GPIO, i2cbus, 0x25, resetPin)    # No more GPIO are consumed for extra MCP devices. Get up to 16x8 MCP I/O.

if not GPIO2.found:
    print ("MCP23017 on %s not detected, or not reset properly" % hex(GPIO2.addr))

# And do some useless I/O test things:

# If following seems to run slow, it is likely that i2c on arduino is timing out on failure to talk with mcp.

# portA (0-7):
GPIO2.setup(3, GPIO.IN)
GPIO2.setup(4, GPIO.OUT)
GPIO2.setup(5, GPIO.IN, GPIO.PUD_UP)
print ("Input 5 (porta:5) with pullup: %d" % GPIO2.input(5))
GPIO2.setup(6, GPIO.IN, GPIO.PUD_DOWN)   # gives a warning. no pulldown function on MCP.
GPIO2.output(4, GPIO.HIGH)

# portB (8-15):
GPIO2.setup(13, GPIO.OUT)
GPIO2.setup(9, GPIO.IN, GPIO.PUD_UP)
print ("Input 9 (portb:1) with pullup: %d" % GPIO2.input(9))
# If pin9 were floating, its input would be erratic. With pullup it should be firmly HIGH
GPIO2.output(13, GPIO.HIGH)
print ("LED ON?")
time.sleep(2)
GPIO2.output(13, GPIO.LOW)
print ("LED OFF?")

time.sleep(2)

print ("1000 pulses on LED ...")
# Speed test
t0 = time.time()
for k in range(1000):
        GPIO2.output(13, GPIO.HIGH)
        GPIO2.output(13, GPIO.LOW)
print ("Done.  %f secs" % (time.time() - t0))
# 6 secs on my laptop virt GPIO
# 2.1 secs on my RPI GPIO
