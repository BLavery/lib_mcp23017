lib_mcp23017
============

Simple python library for MCP23017

## May 2018 - This is no longer being maintained by the original author.
## Please feel free to fork, copy, adapt if you find it useable

For Raspberry Pi (at 3.3V) or "Virtual-GPIO" (at 5V)

A totally simple bit-based I/O class for 16 digital pins on MCP23107. No interrupts, no inversions.
Syntax mirrors regular digital self.GPIO I/O
Supports multiple MCP devices by one MCP23017 object for each

Tie MCP23017's RST: (1) to arduino RST. That resets mcp with each arduino hard or DTR reset.
(2) or simply tied HIGH (not preferred)
(3) or driven from a regular self.GPIO pin to control reset (RPI preference)


Setup:
5V or 3.3V operation.
Tie mcp RST to arduino RST (but see resetPin notes below)
a0 a1 a2 to high (address 0x27) - or as you choose
mcp to arduino    SDA - SDA  and  SCL - SCL      (or equiv on RPI)
RPI has i2c pullups already.
Arduino uses its large internal pullups, marginal. Recomment extra external pullups (eg 4k7).

These MCP pins MUST be connected somewhere: A0 A1 A2 RST SDA SCL VDD/VCC VSS/GND
