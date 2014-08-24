MacroBull's mcu tools
==================

baudCalc.py
-----
Baudrate calculator for msp430.

usage:

	$ baudCalc.py 12000000 460800
	
	Clock=12000000.0Hz, Baudrate=460800
	
	UCA0BR0 = 26;
	UCA0BR1 = 0;
	UCA0MCTL = UCBR0;
	
	#define UCBR0 0b00000000


serialReader.py
--------
My simple serialport tool, with functions of:

* TTY device auto detect; (by [serialChecker](https://github.com/MacroBull/lib-python-macrobull/blob/master/macrobull/misc.py) )
* Timestammp + hex value display;
* 16 bytes per line or '\n' for new line(Text mode);
* Change baudrate;
* Auto send;
* Dump data only / full information to file;
* Terminal/screen mode, send keyboard inputs.

Example:

	$ serialReader -c 460800
	
	serialReader [-c (for text mode)] [-se (for screen + echo mode)] [dump, dump-all] baud=9600 intv=0.5 [data='H' disabled in screen mode]
	
	Text mode
	dev=/dev/ttyUSB0 baudrate=460800
	1408851614.109:  76 61 6c 75 65 3d 30 30 30 30 0a                         value=0000.
	1408851614.109:  76 61 6c 75 65 3d 30 30 30 30 0a                         value=0000.
	1408851614.109:  76 61 6c 75 65 3d 30 30 30 30 0a                         value=0000.
	1408851614.110:  76 61 6c 75 65 3d 30 30 30 30 0a                         value=0000.
	1408851614.110:  76 61 6c 75 65 3d 30 30 30 30 0a                         value=0000.
	^C
	Exited

dataDisp_*
------
Combinations of SerialReader with [DynamicPlot](https://github.com/MacroBull/lib-python-macrobull/blob/master/macrobull/dynamicPlot.py)

Parse the data from serial and plot the values in time.

UT61C_Reader is an example of these, it parses data from UT61x multimeter:

	$ UT61C_Reader
	
	dev=/dev/ttyUSB0 baudrate=2400
	34 21 00 00 20 00 0d 0a 2b 30 30 30 31 20       4!.. ...+0001   0.1     $\Omega  $
	34 21 00 00 20 00 0d 0a 2b 30 30 30 31 20       4!.. ...+0001   0.1     $\Omega  $
	34 21 00 00 20 00 0d 0a 2b 30 30 30 32 20       4!.. ...+0002   0.2     $\Omega  $
	34 21 00 00 20 00 0d 0a 2b 30 30 30 32 20       4!.. ...+0002   0.2     $\Omega  $
	30 31 00 00 80 00 0d 0a 2d 30 30 30 31 20       01......-0001   -1.0    $V (DC)$
	34 31 00 40 80 80 0d 0a 2b 30 30 30 31 20       41.@....+0001   0.0001  $V (DC)$
	34 31 00 40 80 00 0d 0a 2b 30 30 30 30 20       41.@....+0000   0.0     $V (DC)$
	34 31 00 40 80 00 0d 0a 2d 30 31 33 38 20       41.@....-0138   -0.0138         $V (DC)$
	34 31 00 40 80 82 0d 0a 2d 30 32 39 39 20       41.@....-0299   -0.0299         $V (DC)$
	34 31 00 40 80 83 0d 0a 2d 30 33 37 38 20       41.@....-0378   -0.0378         $V (DC)$





	
UT61C_Reader.py : Derived from serialReader, for reading data via serial port from .

rawData.py : Derived from serialReader, plot serail data by byte.
