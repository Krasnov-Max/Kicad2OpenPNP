#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

parser = argparse.ArgumentParser(description='Convert Kicad footprint files to xml file for OpwnPNP')
parser.add_argument('infile', type=str, help='Input Kicad footprint file')
parser.add_argument('outfile', type=str, help='Output file xml format')
args = parser.parse_args()
print(args.infile)
print(args.outfile)

fin = open(args.infile, 'r')
fout = open(args.outfile, 'w')
buf = ''
name_comp = ''
name = ''
x = ''
y = ''
sx = ''
sy = ''
file = ''
for Line in fin:
    result = re.search(r'\(footprint\s\"\S*\"', Line)
    if (result !=None) :
        print (Line)
        tmp = result.group(0)
        result = re.search(r'\"\S*\"',Line)
        if (result !=None):
            tmp = result.group(0)
            result = re.split(r'\"',tmp)
            if (result !=None):
                name_comp = result[1]
                print("Name is component: ",name_comp)
fin.close                

packages = ET.Element("openpnp-packages")
package = ET.SubElement(packages, "package", version="1.1", id=name_comp)
footprint = ET.SubElement(package, "footprint", units="Millimeters")
fin = open(args.infile, 'r')                

for Line in fin:                
    result = re.search(r'pad\s\"\d{1,}\"\s', Line)
    if (result !=None) :
        result = re.search(r'\d{1,}',Line)
        name = result.group(0) 
        print("Pad name: ",name)
        result = re.search(r'\(at\s\-?\d{1,}\.?\d{1,}\s\-?\d{1,}\.*\d?\d?\d?\d?\)', Line)
        if (result !=None):
            tmp = result.group(0)
            result = re.search(r'\-?\d{1,}\.?\d{1,}\s\-?\d{1,}\.*\d?\d?\d?\d?', tmp)
            if (result !=None):
                tmp = result.group(0)
                result = re.split('\s', tmp)
                if (result !=None):
                    x = result[0]
                    y = result[1]
                    print("X cord:",x," Y cord:",y)    
        result = re.search(r'\(size\s\-?\d{1,}\.?\d{1,}\s\d{1,}\.*\d?\d?\d?\d?\)',Line)            
        if (result !=None):
            tmp = result.group(0)
            result = re.search(r'\-?\d{1,}\.?\d{1,}\s\d{1,}\.*\d?\d?\d?\d?', tmp)
            if (result !=None):
                tmp = result.group(0)
                result = re.split(r'\s', tmp)
                if (result !=None):
                    sx = result[0]
                    sy = result[1]
                    print("X size:",sx," Y size:",sy)    
        ET.SubElement(footprint, "pad", name=name, x=x, y=y, width=sx, height=sy, rotation="0.0", roundness="0.0")


#printt(Line)
xml_str = minidom.parseString(ET.tostring(packages)).toprettyxml(indent="   ")
xml_lines = xml_str.splitlines()
xml_str = "\n".join(xml_lines[1:]) # Remove XML declaration
                    
fout.write(xml_str)
fin.close
fout.close


#<package version="1.1" id="LED 5050" pick-vacuum-level="0.0" place-blow-off-level="0.0">
#      <footprint units="Millimeters" body-width="0.0" body-height="0.0">
#         <pad name="1" x="-2.4" y="-1.7" width="1.1" height="2.0" rotation="90.0" roundness="0.0"/>
#         <pad name="2" x="-2.4" y="0.0" width="1.1" height="2.0" rotation="90.0" roundness="0.0"/>
#         <pad name="3" x="-2.4" y="1.7" width="1.1" height="2.0" rotation="90.0" roundness="0.0"/>
#         <pad name="4" x="2.4" y="1.7" width="1.1" height="2.0" rotation="90.0" roundness="0.0"/>
#         <pad name="5" x="2.4" y="0.0" width="1.1" height="2.0" rotation="90.0" roundness="0.0"/>
#         <pad name="6" x="2.4" y="-1.7" width="1.1" height="2.0" rotation="90.0" roundness="0.0"/>
#      </footprint>
#      <compatible-nozzle-tip-ids class="java.util.ArrayList">
#         <string>TIP172ad9ccb63269d3</string>
#      </compatible-nozzle-tip-ids>
#   </package>