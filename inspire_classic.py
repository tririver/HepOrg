#!/usr/bin/python3

import sys
import refio

htm_file_name = sys.argv[1]
org_file_name = 'classic.org'
refio.main(htm_file_name, org_file_name, dl='T', parser='inspire')
