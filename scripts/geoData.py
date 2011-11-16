from xml.dom import minidom
from time import sleep
import urllib
import MySQLdb
import os

# This script gets an IP from the BBDD and searches for the geolocation data

geoDataServer = 'http://api.hostip.info/?ip='
geoDataTmpFile = 'geoData.xml'


def getRawGeoDataByIp(ip):
    try:
        urllib.urlretrieve(geoDataServer+ip,geoDataTmpFile)
        xmldoc = minidom.parse(geoDataTmpFile) 
        print geoDataServer+ip
        country = xmldoc.getElementsByTagName('countryAbbrev')[0].childNodes[0].nodeValue
        print "Country: " + country
        lat = ""
        lng = ""
        if(country!="XX"):
            coordinates = xmldoc.getElementsByTagName('gml:coordinates')
            if(coordinates):
                for coord in coordinates:    
                    latlng = coord.firstChild.nodeValue            
                lat,lng = latlng.split(",")
                saveData(lat,lng,country, ip)
            else:
                print "no coords"
                saveCountry(country, ip)
        else:
            print "update fail"
            updateFail(ip)
        os.remove(geoDataTmpFile)
    
    #TODO: When checking the geolocation if fails we have to flag that
    # catch the exception and save it as a failure.
    # write a different process to handle failures
    except:
        updateFail(ip)
    finally:
        return
    
def updateFail(ip):
    try: 
        conn = MySQLdb.connect('localhost','section9', 'section9', 'section9');
        cursor = conn.cursor()
        cursor.execute("""
                            UPDATE geoipdata 
                            SET failed= 1, complete = 0
                            WHERE ip = %s """, ip)
        cursor.close()
        conn.commit()
        conn.close()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        return
    
def saveCountry(country, ip):
    try:
        conn = MySQLdb.connect('localhost','section9', 'section9', 'section9');
        cursor = conn.cursor()
        cursor.execute("""
                            UPDATE geoipdata 
                            SET country = %s, complete = 1, failed2 = 1
                            WHERE ip = %s """, (country, ip))
        cursor.close()
        conn.commit()
        conn.close()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        return



def saveData(lat, long, country, ip):
    try:
        conn = MySQLdb.connect('localhost','section9', 'section9', 'section9');
        cursor = conn.cursor()
        cursor.execute("""
                            UPDATE geoipdata 
                            SET latitude = %s, longitude = %s, country = %s, complete = 1, failed = 0, failed2 = 0
                            WHERE ip = %s """, (lat, long, country, ip))
        cursor.close()
        conn.commit()
        conn.close()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        return

def geoLocateIps():
    try:
        conn = MySQLdb.connect('localhost','section9', 'section9', 'section9');
        cursor = conn.cursor()
        sSql = """SELECT ip FROM geoipdata WHERE  complete is null"""
        cursor.execute(sSql)
        rows = cursor.fetchall()
        for row in rows:
            checkLocalDb(row[0])
        
        sSql = """SELECT ip FROM geoipdata WHERE  failed = 1"""
        cursor.execute(sSql)
        rows = cursor.fetchall()
        for row in rows:
            getRawGeoDataByIp(row[0])
            sleep(1)
        
        cursor.close()
        conn.commit()
        conn.close()
        
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:
        return

def checkLocalDb(ip):
    try:
        conn = MySQLdb.connect('localhost','section9', 'section9', 'section9');
        cursor = conn.cursor()
        cursor.execute("""SELECT 
                                    locations.longitude, locations.latitude,locations.country_code, ip_group_city.location 
                            FROM ip_group_city,locations 
                            WHERE ip_start <= INET_ATON(%s) 
                            AND ip_group_city.location = locations.id 
                            ORDER BY ip_start DESC LIMIT 1;
                            """, (ip))
        rows = cursor.fetchall()
        for row in rows:
             lng = row[0]
             lat = row[1]
             country = row[2]
             location = row[3]
             saveData(lat,lng,country,ip)
        cursor.close()
        conn.commit()
        conn.close()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        return

geoLocateIps()

