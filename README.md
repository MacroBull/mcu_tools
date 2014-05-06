MacroBull's mcu tools
==================

baudCalc.py : Calculate baudrate for msp430, this feature is add in my msp430 lib and no longer needed.

serialReader.py :  depend on my python lib [ https://github.com/MacroBull/lib-python-macrobull ]
	-c (for text mode) 
	-s / -se (for screen mode, directly send input keys like "screen", -se for displaying input to screen) 
	dump / dump-all (dump data to file, all for hex+text both)
	baud=9600 
	intv=0.5 
	data='H' (auto send data, disabled in screen mode)
	
UT61C_Reader.py : Derived from serialReader, for reading data via serial port from UT61x multimeter.

rawData.py : Derived from serialReader, plot serail data by byte.
