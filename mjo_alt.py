#!/usr/bin/env python3
import argparse,sys
from staralt import *


if __name__ == '__main__':
	parser = argparse.ArgumentParser(usage="Makes an altitude plot for a given target and date")
	parser.add_argument('ra', help=('RA in either hourangle or degrees'))
	parser.add_argument('dec', help=('Dec in either hourangle or degrees'))
	parser.add_argument('-date', default=None, help=('Date of the observation'))
	parser.add_argument('-name',default='Target',type=str, help=('RA in either hourangle or degrees'))
	parser.add_argument('-plot', default = True, type=bool, help=('RA in either hourangle or degrees'))

	args = parser.parse_args()
	print('have arguments')
	observatory = Observatory()
	date = Date(date=args.date)
	target = Target(ra = args.ra, dec = args.dec, date = date)
	altitudes = Altitudes(observatory, date, target)
	Visibility(altitudes, date, plot = args.plot)

