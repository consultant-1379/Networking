#!/usr/bin/python

###################################################################################################
###################################### SCRIPT INFORMATION : #######################################
############################### Eoin O'Sullivan (eeoiosu) Apr 2019 ################################
###################################################################################################
###          This is a test script to calculate the subnet range of a given ip address          ###
###################################################################################################

#~# Includes #~#
import os
import json
import csv
import ipaddress
#~# Global Variables
IP_ADDRESS = '10.151.222.37/27'
#~#
class SUBNET_RANGE_Inventory(object):
    #------------------------------------------------------
    def __init__(self):
        self.inventory = {
            'ip_address': IP_ADDRESS
        }
        self.calculate_subnet()
        self.display_output()
    #------------------------------------------------------
    def calculate_subnet(self):
        net = ipaddress.ip_network(unicode(IP_ADDRESS, "utf-8"), strict=False)
        self.inventory['subnet_range'] = net.with_prefixlen
    #------------------------------------------------------
    def display_output(self):
        print(self.json_format_dict(self.inventory, True))
    #------------------------------------------------------
    def json_format_dict(self, data, pretty=False):
        #~# Converts a dict to a JSON object and dumps it as a formatted string
        if pretty:
            return json.dumps(data, sort_keys=True, indent=2)
        else:
            return json.dumps(data)
    #------------------------------------------------------
#~#
SUBNET_RANGE_Inventory()