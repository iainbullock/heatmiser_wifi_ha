#!/usr/bin/env python
# coding=utf-8
#
###############################################################################
#   - heatmiser_wifi -
#
#   Copyright 2020 by Joel Midstjärna (joel.midstjarna@gmail.com)
#
#   A Heatmiser WiFi Thermostat communication library. 
#
#   Supported Heatmiser Thermostats orignally were DT, DT-E, PRT and PRT-E.
#
#   Update by Iain Bullock Feb 2023 to add support for PRTHW, 
#   and to be able to read and write more things 
#
#   It is also possible to run this file as a command line executable.
#
#   All rights reserved.
#   This file is part of the heatmiser_wifi python library and is
#   released under the "MIT License Agreement". Please see the LICENSE
#   file that should have been included as part of this package.
###############################################################################

import socket, time, sys
from optparse import OptionParser
from collections import OrderedDict
from datetime import datetime

class CRC16:
    CRC16_LookupHigh = [0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70,
                        0x81, 0x91, 0xA1, 0xB1, 0xC1, 0xD1, 0xE1, 0xF1]
    CRC16_LookupLow  = [0x00, 0x21, 0x42, 0x63, 0x84, 0xA5, 0xC6, 0xE7,
                        0x08, 0x29, 0x4A, 0x6B, 0x8C, 0xAD, 0xCE, 0xEF]
                        
    CRC16_High = 0xff
    CRC16_Low  = 0xff
    
    def _CRC16_Update4Bits(self, val):
        t = (self.CRC16_High >> 4) & 0xff
        t = (t ^ val) & 0xff
        self.CRC16_High = ((self.CRC16_High << 4)|(self.CRC16_Low >> 4)) & 0xff
        self.CRC16_Low  = (self.CRC16_Low << 4) & 0xff
        self.CRC16_High = (self.CRC16_High ^ self.CRC16_LookupHigh[t]) & 0xff
        self.CRC16_Low  = (self.CRC16_Low  ^ self.CRC16_LookupLow[t]) & 0xff
        
    def _CRC16_Update(self, val):
        self._CRC16_Update4Bits((val >> 4) & 0x0f)
        self._CRC16_Update4Bits(val & 0x0f)
        
    def CRC16(self,bytes):
        self.CRC16_High = 0xff
        self.CRC16_Low  = 0xff
        for byte in bytes:
            self._CRC16_Update(byte)
        return (self.CRC16_Low, self.CRC16_High)
    

class HeatmiserTransport:
    ''' This class handles the Heatmiser transport protocol '''
    def __init__(self, host, port, pin):
        self.host = host
        self.port = port
        self.crc16 = CRC16()
        self.pin = pin
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        self.sock.settimeout(5)
        
    def disconnect(self):
        self.sock.close()
        
    def _send_read_request(self, dcb_start = 0x0, dcb_length = 0xffff):
        ''' dcb_length = 0xffff means the whole DCB. The Heatmiser v3 protocol
            specification recommends that the whole DCB shall be read at once.
            It seems that dcb_start > 0x0 has no effect.
        '''
        frame_list = [
            0x93,              # Operation 0x93=Read, 0xa3=Write
            0x0b,              # Frame length low byte inc CRC (0xb if no data)
            0x00,              # Frame length high byte inc CRC (0 if no data)
            int(self.pin) & 0xff,   # PIN code low byte
            int(self.pin) >> 8,     # PIN code high byte
            dcb_start & 0xff,  # DCB start low byte 
            dcb_start >> 8,    # DCB start high byte 
            dcb_length & 0xff, # DCB length low byte  (0xff for whole DCB)
            dcb_length >> 8]   # DCB length high byte (0xff for whole DCB) 
        frame = bytearray(frame_list)
        
        # Add CRC16 to the frame (16 bytes)
        (crc16_low, crc16_high) = self.crc16.CRC16(frame)
        frame.append(crc16_low)
        frame.append(crc16_high)       
        
        self.sock.send(frame)
        
    def _send_write_request(self, dcb_address, dcb_data):
        ''' dcb_address is address in DCB block (not index) '''
        dcb_length = len(dcb_data)
        length = dcb_length + 11
        frame_list = [
            0xa3,              # Operation 0x93=Read, 0xa3=Write
            length & 0xff,     # Frame length low byte inc CRC (11+dcb_data)
            length >> 8,       # Frame length high byte inc CRC (11+dcb_data)
            self.pin & 0xff,   # PIN code low byte
            self.pin >> 8,     # PIN code high byte
            1,                 # Nbr of items (only 1 in this impl)
            dcb_address & 0xff,# DCB address low byte 
            dcb_address >> 8,  # DCB address high byte 
            dcb_length]        # DCB length
        frame = bytearray(frame_list) + dcb_data
        
        # Add CRC16 to the frame (16 bytes)
        (crc16_low, crc16_high) = self.crc16.CRC16(frame)
        frame.append(crc16_low)
        frame.append(crc16_high)       
        
        self.sock.send(frame)        
        
    def _receive_dcb(self):
        data = self.sock.recv(1024)
        frame = bytearray(data)
        
        # Validate the CRC (two last bytes) and remove from frame
        received_crc16_high = frame.pop()
        received_crc16_low = frame.pop()
        (crc16_low, crc16_high) = self.crc16.CRC16(frame)
        if((received_crc16_high != crc16_high) or (received_crc16_low != crc16_low)):
            raise Exception("CRC16 mismatch in received data from Thermostat")
            
        # Validate frame head
        if(frame[0] != 0x94):
             raise Exception("Unknown type of message received from Thermostat")
             
        # Read out and validate the frame length
        frame_length = (frame[2] << 8) | frame[1]
        if(frame_length != (len(frame) + 2)): #+2 since CRC has been removed
            raise Exception("Invalid frame length in data received from Thermostat")
        
        # Read out DCB start address
        dcb_start = (frame[4] << 8) | frame[3]
        
        # Read out and validate DCB content length
        dcb_length = (frame[6] << 8) | frame[5]
        if(dcb_length == 0):
            raise Exception("Thermostat connected but reports wrong PIN code")
        if(dcb_length != (frame_length - 9)): #Overhead in frame is 9 bytes
            raise Exception("Invalid DCB length in data received from Thermostat")            
            
        # Read out DCB data
        dcb_data = frame[7:]
             
        return (dcb_start, dcb_data)
    
    def get_dcb(self):
        ''' Get whole DCB '''
        self._send_read_request()
        (dcb_start, dcb_data) = self._receive_dcb()
        return dcb_data
        
    def set_dcb(self, dcb_address, dcb_data):
        self._send_write_request(dcb_address, dcb_data)
        # Just get an ACK from the Thermostat (don't use the result)
        dcb = self._receive_dcb()

class Heatmiser(HeatmiserTransport):
    ''' This class handles the Heatmiser application (DCB) protocol '''
    
    def _get_info_time_triggers(self, dcb, first_index):
        index = first_index
        info = OrderedDict()
        for i in range (1,5):
            trigger = OrderedDict()
            trigger['hour'] = dcb[index]
            index = index + 1
            trigger['minute'] = dcb[index]
            index = index + 1     
            trigger['set_temp'] = dcb[index]
            index = index + 1
            info['time'+str(i)] = trigger
         
        return info 
    
    def get_info(self):
        ''' Returns an ordered dictionary with all Thermostat values '''
        dcb = self.get_dcb()
        
        if(len(dcb) < 41):
            raise Exception("Size of DCB received from Thermostat is too small")
        
        info = OrderedDict()
        
        if(dcb[2] == 0):
            info["vendor_id"] = "HEATMISER"
        else:
            info["vendor_id"] = "OEM"           
        info["version"] = dcb[3] & 0x7F  
        info["in_floor_limit_state"] = ((dcb[3] & 0x8F) > 0)
        if(dcb[4] == 0):
            info["model"] = "DT"
        elif(dcb[4] == 1):
            info["model"] = "DT-E"       
        elif(dcb[4] == 2):
            info["model"] = "PRT" 
        elif(dcb[4] == 3):
            info["model"] = "PRT-E"
        elif(dcb[4] == 4):
            info["model"] = "PRTHW"
        else:
            info["model"] = "Unknown"
        if(dcb[5] == 0):
            info["temperature_format"] = "Celsius"
        else:
            info["temperature_format"] = "Fahrenheit"
        info["switch_differential"] = dcb[6]
        info["frost_protection_enable"] = (dcb[7] == 1)
        info["calibration_offset"] = ((dcb[8] << 8) | dcb[9])
        info["output_delay_in_minutes"] = dcb[10]
        # dcb[11] = address (not used)
        info['up_down_key_limit'] = dcb[12]
        if(dcb[13] == 0):
            info['sensor_selection'] = "Built in air sensor only"
        elif(dcb[13] == 1):
            info['sensor_selection'] = "Remote air sensor only"
        elif(dcb[13] == 2):
            info['sensor_selection'] = "Floor sensor only"
        elif(dcb[13] == 3):
            info['sensor_selection'] = "Built in air and floor sensor"
        elif(dcb[13] == 4):
            info['sensor_selection'] = "Remote air and floor sensor"
        else:
            info['sensor_selection'] = "Unknown"
        info['optimum_start'] = dcb[14]
        info['rate_of_change'] = dcb[15]
        if(dcb[16] == 0):
            info['program_mode'] = "2/5 mode"
        else:
            info['program_mode'] = "7 day mode"
        info['frost_protect_temperature'] = dcb[17]
        info['set_room_temp'] = dcb[18]
        info['floor_max_limit'] = dcb[19]
        info['floor_max_limit_enable'] = (dcb[20] == 1)
        if(dcb[21] == 1):
            info['on_off'] = "On"
        else:
            info['on_off'] = "Off"
        if(dcb[22] == 0):
            info['key_lock'] = "Unlock"
        else:
            info['key_lock'] = "Lock"  
        if(dcb[23] == 0):
            info['run_mode'] = "Heating mode (normal mode)"
        else:
            info['run_mode'] = "Frost protection mode"
        info['away_mode'] = dcb[24]
        info['holiday_return_date_year'] = 2000 + dcb[25]
        info['holiday_return_date_month'] = dcb[26]
        info['holiday_return_date_day_of_month'] = dcb[27]
        info['holiday_return_date_hour'] = dcb[28]
        info['holiday_return_date_minute'] = dcb[29]
        info['holiday_enable'] = (dcb[30] == 1)
        info['temp_hold_minutes'] = ((dcb[31] << 8) | dcb[32])
        if((dcb[13] == 1) or (dcb[13] == 4)):
            info['air_temp'] = (float((dcb[34] << 8) | dcb[33]) / 10.0)   
        if((dcb[13] == 2) or (dcb[13] == 3) or (dcb[13] == 4)):
            info['floor_temp'] = (float((dcb[36] << 8) | dcb[35]) / 10.0)               
        if((dcb[13] == 0) or (dcb[13] == 3)):
            info['air_temp'] = (float((dcb[38] << 8) | dcb[37]) / 10.0)
        info['error_code'] = dcb[39]
        info['heating_is_currently_on'] = (dcb[40] == 1)
        
        # Model DT and DT-E stops here
        if(dcb[4] <= 1):
            return info
        
        if(len(dcb) < 72):
            raise Exception("Size of DCB received from Thermostat is too small")        

        # Model PRTHW  has extra fields and adds an offset for the rest
        if(dcb[4] == 4):
            info['hot_water'] = dcb[43]
            offset = 3
        else:
            offset = 0
 
        info['year'] = 2000 + dcb[41 + offset]
        info['month'] = dcb[42 + offset]
        info['day_of_month'] = dcb[43 + offset]
        info['weekday'] = dcb[44 + offset]
        info['hour'] = dcb[45 + offset]
        info['minute'] = dcb[46 + offset]
        info['second'] = dcb[47 + offset]
        info['date_time'] = str(info['year']) + '/' + str(info['month']) + '/' + str(info['day_of_month']) + " " + str(info['hour']) + ':' + str(info['minute']) + ':' + str(info['second'])

        info['weekday_triggers'] = self._get_info_time_triggers(dcb, 48 + offset)
        info['weekend_triggers'] = self._get_info_time_triggers(dcb, 60 + offset)
        
        # If mode is 5/2 stop here
        if(dcb[16] == 0):
            return info      
            
        if(len(dcb) < 156):
            raise Exception("Size of DCB received from Thermostat is too small")    
            
        # Theses offsets are incorrect. Need to figure out how much of the DCB the hot water times take and make a further adjustment
        info['mon_triggers'] = self._get_info_time_triggers(dcb, 72 + offset) 
        info['tue_triggers'] = self._get_info_time_triggers(dcb, 84 + offset) 
        info['wed_triggers'] = self._get_info_time_triggers(dcb, 96 + offset)
        info['thu_triggers'] = self._get_info_time_triggers(dcb, 108 + offset)
        info['fri_triggers'] = self._get_info_time_triggers(dcb, 120 + offset) 
        info['sat_triggers'] = self._get_info_time_triggers(dcb, 132 + offset)
        info['sun_triggers'] = self._get_info_time_triggers(dcb, 144 + offset)   
        
        return info

    def set_value(self, name, value):
        ''' Use the same name and value as returned in get_info. Only a few
            name/keys are supported in this implementation. Use the set_dcb
            method to set any value. '''
        if(name == "switch_differential"):
            self.set_dcb(6,bytearray([int(value)]))
        elif(name == "frost_protect_temperature"):
            self.set_dcb(17,bytearray([int(value)]))            
        elif(name == "set_room_temp"):
            self.set_dcb(18,bytearray([int(value)]))  
        elif(name == "floor_max_limit"):
            self.set_dcb(19,bytearray([int(value)]))  
        elif(name == "floor_max_limit_enable"):
            if((value == True) or (value == "True") or (value == "1") or (value == 1)):
                value = 1
            elif((value == False) or (value == "False") or (value == "0") or (value == 0)):
                value = 0
            else:
                raise Exception("'"+name+"' invalid value '"+str(value)+"'\n" +
                                "Valid values: True, 1, False or 0")
            self.set_dcb(20,bytearray([value]))  
        elif(name == "on_off"):
            if(value == "On"):
                value = 1
            elif(value == "Off"):
                value = 0
            else:
                raise Exception("'"+name+"' invalid value '"+str(value)+"'\n" +
                                "Valid values: 'On' or 'Off'")
            self.set_dcb(21,bytearray([value])) 
        elif(name == "key_lock"):
            if(value == "Lock"):
                value = 1
            elif(value == "Unlock"):
                value = 0
            else:
                raise Exception("'"+name+"' invalid value '"+str(value)+"'\n" +
                                "Valid values: 'Lock' or 'Unlock'")
            self.set_dcb(22,bytearray([value]))
        elif(name == "run_mode"):
            if(value == "Frost protection mode"):
                value = 1
            elif(value == "Heating mode (normal mode)"):
                value = 0
            else:
                raise Exception("'"+name+"' invalid value '"+str(value)+"'\n" +
                                "Valid values: 'Frost protection mode' or " +
                                "'Heating mode (normal mode)'")
            self.set_dcb(23,bytearray([value]))                            
        elif(name == "away_mode"):
            if(value == "off"):
                value = 0
            elif(value == "on"):
                value = 1
            else:
                raise Exception("'"+name+"' invalid value '"+str(value)+"'\n" +
                                "Valid values: 'on' or 'off'")
            self.set_dcb(31,bytearray([value]))
        elif(name == "hot_water"):
            if(value == "off"):
                value = 0
            elif(value == "on"):
                value = 1
            else:
                raise Exception("'"+name+"' invalid value '"+str(value)+"'\n" +
                                "Valid values: 'on' or 'off'")
            self.set_dcb(42,bytearray([value]))
        elif(name == "date_time"):
            # ignore passed value, use system time
            todays_date = datetime.now()
            self.set_dcb(43,bytearray([todays_date.hour]))
        else:
            raise Exception("'"+name+"' not supported to be set")




###############################################################################
# Below is a command line tool for reading and setting parameters of a
# Heatmiser Wifi thermostat. It can also be seen as an example on how to use
# the library.


def print_dict(dict, level=""):
    for i in dict.items():
        if(isinstance(i[1],OrderedDict)):
            print(level+i[0]+":")
            print_dict(i[1],level + "    ")
        else:
            print(level+str(i[0])+" = "+str(i[1]))
        
def main():
    # This function shows how to use the Heatmiser class. 
    
    parser = OptionParser("Usage: %prog [options] <Heatmiser Thermostat address>")
    parser.add_option("-p", "--port", dest="port", type="int",
                      help="Port of HeatMiser Thermostat (default 8068)", default=8068) 
    parser.add_option("-c", "--pin", dest="pin", type="int",
                      help="Pin code of HeatMiser Thermostat (default 0000)", default=0)
    parser.add_option("-l", "--list", action="store_true", dest="list_all",
                      help="List all parameters in Thermostat", default=False)
    parser.add_option("-r", "--read",  dest="parameter",
                      help="Read one parameter in Thermostat (-r param)", default="")
    parser.add_option("-w", "--write",  dest="param_value", nargs=2,
                      help="Write value to parameter in Thermostat (-w param value)")                       
    (options, args) = parser.parse_args()
    
    if (len(args) != 1):
        parser.error("Wrong number of arguments")
    
    host = args[0]
                      
    # Create a new Heatmiser object
    heatmiser = Heatmiser(host,options.port,options.pin)
    
    # Connect to Thermostat
    heatmiser.connect()
    
    # Read all parameters
    info = heatmiser.get_info()
    
    # Print all parameters in Thermostat
    if(options.list_all):
        print_dict(info)
        
    # Print one parameter in Thermostat
    if(options.parameter != ""):
        if (options.parameter in info):
            print(options.parameter + " = " + str(info[options.parameter]))
        else:
            sys.stderr.write("Error!\n"+
                "Parameter '"+options.parameter+"' does not exist\n")
    
    # Write value to one parameter in Thermostat
    if(options.param_value != None):
        param = options.param_value[0]
        value = options.param_value[1]
        if (param in info):
            try:
                heatmiser.set_value(param,value)
                info2 = heatmiser.get_info()
                print("Before change: " + param + " = " + str(info[param]))
                print("After change:  " + param + " = " + str(info2[param]))
            except Exception as e:
                sys.stderr.write(e.args[0]+"\n")
        else:
            sys.stderr.write("Error!\n"+
                "Parameter '"+param+"' does not exist\n")
    heatmiser.disconnect()
        
if __name__ == '__main__':
    main()    