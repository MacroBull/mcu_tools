# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 15:14:59 2014
Project	:Python-Project
Version	:0.0.1
@author	:macrobull

"""


x=0
y=1
a=[0]
for i in range(10):
	a.append(y*0.3+a[-1]*0.7)

from pylab import *
plot(a)
show()