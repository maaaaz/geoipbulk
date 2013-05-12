#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of geoipbulk.
#
# Copyright (C) 2013, Thomas Debize <tdebize at mail.com>
# All rights reserved.
#
# geoipbulk is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# geoipbulk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with geoipbulk.  If not, see <http://www.gnu.org/licenses/>.

import re, sys, csv, socket, struct

# GeoIP import
try :
	import GeoIP
	GEOIP = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
except ImportError :
	print "[!] The GeoIP python library seems to be missing..."
	print "[!] You have to install it. Try 'apt-get install python-geoip' or get 'http://www.maxmind.com/download/geoip/api/python/GeoIP-Python-latest.tar.gz'"
	sys.exit(1)

# OptionParser imports
from optparse import OptionParser

# Options definition
option_0 = { 'name' : ('-i', '--input'), 'help' : 'IP list file (stdin if not specified)', 'nargs' : 1 }
option_1 = { 'name' : ('-o', '--output'), 'help' : 'csv output filename (stdout if not specified)', 'nargs' : 1 }
option_2 = { 'name' : ('-c', '--count'), 'help' : 'count IP occurence', 'action' : 'store_true', 'default' : False}
option_3 = { 'name' : ('-r', '--reverse'), 'help' : 'reverse sort order', 'action' : 'store_true', 'default' : False }
option_4 = { 'name' : ('-s', '--skip-header'), 'help' : 'do not print the csv header', 'action' : 'store_true', 'default' : False }

options = [option_0, option_1, option_2, option_3, option_4]

# Handful IP regex
p_ip = re.compile('(?P<ip>%s)' % '(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})')

# Handful functions
def dottedquad_to_num(ip):
	"""
		Convert decimal dotted quad string IP to long integer
	"""
	return struct.unpack('!L',socket.inet_aton(ip))[0]

def count_ip(collection, ip_num):
	"""
		Count number of occurence for an IP (numerical format) into the existing collection
	"""
	result = 0

	if ip_num in collection.keys() :
		num = collection[ip_num]['count']
		result = num + 1
	else :
		result = 1
	
	return result
	
def geo_ip_lookup(ip_address):
	"""
		Retrieve some information related to the IP address passed in, with GeoIP
	"""
	global GEOIP
	
	country_code = GEOIP.country_code_by_addr(ip_address)
	country_name = GEOIP.country_name_by_addr(ip_address)
	
	return country_code, country_name

def parse(fd):
	"""
		Parsing the IP list provided
	"""
	collection = {}
	
	for line in fd:
		line = line.rstrip()
		
		ip = p_ip.search(line)
		if ip:
			ip_dotted = ip.group('ip')
			ip_num = dottedquad_to_num(ip_dotted)
			country_code, country_name = geo_ip_lookup(ip_dotted)
			
			num_occurence = count_ip(collection, ip_num)
			collection[ip_num] = {	'ip_dotted' : ip_dotted, 
									'country_code' : country_code,
									'country_name' : country_name,
									'count' : num_occurence } 
			
	return collection

def generate_csv(fd, results, option_count, option_reverse, option_skip_header) :
	"""
		Generate the output according to the desired options
	"""
	if results != {} :
		spamwriter = csv.writer(fd, delimiter=';')
		
		csv_header = ['COUNT', 'IP', 'COUNTRY_NAME'] if option_count else ['IP', 'COUNTRY_NAME']
		
		if not(option_skip_header) :
			spamwriter.writerow(csv_header)
		
		# Filtering from the counted value or the ip value
		key = lambda ip_num:results[ip_num]['count'] if option_count else lambda ip_num:ip_num
		results_order = sorted(results.iterkeys(),key=key, reverse=option_reverse)
		
		for IP in results_order :
			line_to_write = [results[IP]['count'], results[IP]['ip_dotted'], results[IP]['country_name']] if option_count else [results[IP]['ip_dotted'], results[IP]['country_name']]
			spamwriter.writerow(line_to_write)
	
	return
	
def main(options, arguments):
	# Input descriptor
	if (options.input != None):
		fd_input = open(options.input, 'rb')
	else :
		# No input file specified, reading from stdin
		fd_input = sys.stdin
	
	results = parse(fd_input)
	fd_input.close()
	
	# Output descriptor
	if (options.output != None):
		fd_output = open(options.output, 'wb')
	else :
		# No output file specified, writing to stdout
		fd_output = sys.stdout

	# CSV output
	generate_csv(fd_output, results, options.count, options.reverse, options.skip_header)
	fd_output.close()

	return


if __name__ == "__main__" :
	parser = OptionParser()
	for option in options:
		param = option['name']
		del option['name']
		parser.add_option(*param, **option)

	options, arguments = parser.parse_args()
	main(options, arguments)