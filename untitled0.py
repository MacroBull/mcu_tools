# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 12:04:55 2014
Project	:Python-Project
Version	:0.0.1
@author	:macrobull

"""

XINIF = 1e6
YINIF = 1e6

def proj(p0, p1, p2, p3):
	x0, y0 = p0
	x1, y1 = p1
	x2, y2 = p2
	x3, y3 = p3

	parr_s = parr_t = 0

	denom = (y1 - y0) * (x3 - x2) - (y2 - y3) * (x0 - x1)
	if denom == 0:
		parr_s = 1
	else:
		numx = (x2*y3 - x3*y2) * (x0 - x1) - (x1*y0 - x0*y1) * (x3 - x2)
		numy = (x2*y3 - x3*y2) * (y1 - y0) - (x1*y0 - x0*y1) * (y2 - y3)
		xs = numx / denom
		ys = numy / -denom

	denom = (y1 - y0) * (x3 - x2) - (y2 - y3) * (x0 - x1)
	if denom == 0:
		parr_s = 1
	else:
		numx = (x2*y3 - x3*y2) * (x0 - x1) - (x1*y0 - x0*y1) * (x3 - x2)
		numy = (x2*y3 - x3*y2) * (y1 - y0) - (x1*y0 - x0*y1) * (y2 - y3)
		xs = numx / denom
		ys = numy / -denom

	print xs, ys


	return p0



proj((0,0), (1,2), (0,3), (-1,2))