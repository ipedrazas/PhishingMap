from xml.dom import minidom 
import urllib
import os


xmlFile = 'ips.xml'
txtFile = 'ips.txt'

target = "http://data.phishtank.com/data/online-valid.xml"

urllib.urlretrieve(target,xmlFile)
print('Xml File downloaded')
xmldoc = minidom.parse(xmlFile) 
reflist = xmldoc.getElementsByTagName('ip_address')      

print('Parsing XML')
ipsCol = []
for ips in reflist:    
    ipsCol.append(ips.firstChild.nodeValue)

ipsSet = set(ipsCol)
    
xmlBody = '\n'.join([ipclean for ipclean in ipsSet])

xmlBody = xmlBody + '\n##EOF##'

print('Writing ips in cvs')

myfile = open(txtFile, "w") 
myfile.write(xmlBody )
myfile.close()

print('Removing xml file')
os.remove(xmlFile)